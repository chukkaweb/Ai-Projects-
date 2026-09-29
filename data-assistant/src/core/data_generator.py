"""
Data generation orchestration module.
"""

import pandas as pd
from typing import Dict, List, Any, Optional
from llm.gemini_client import GeminiClient, _is_transient_error
from core.ddl_parser import SchemaParser
from core.db import db_manager
from observability.langfuse_tracing import logger


class DataGenerator:
    """Orchestrates synthetic data generation process."""
    
    def __init__(self, temperature: float = 0.7, max_tokens: int = 8192):
        """
        Initialize data generator.
        
        Args:
            temperature: Temperature for Gemini generation
            max_tokens: Maximum output tokens for Gemini generation
        """
        self.gemini_client = GeminiClient(temperature=temperature, max_tokens=max_tokens)
        self.schema_parser = SchemaParser()
    
    def generate_data(
        self,
        ddl_content: str,
        instructions: str,
        num_rows: int,
        temperature: float = 0.7,
        max_tokens: int = 8192
    ) -> Dict[str, pd.DataFrame]:
        """
        Generate synthetic data from DDL schema.
        Uses batch generation for large datasets to avoid JSON parsing issues.
        
        Args:
            ddl_content: SQL DDL content
            instructions: User instructions for generation
            num_rows: Number of rows to generate
            temperature: Generation temperature
            max_tokens: Maximum output tokens
            
        Returns:
            Dictionary mapping table names to DataFrames
        """
        try:
            # Update temperature or max_tokens if changed
            if temperature != self.gemini_client.temperature or max_tokens != self.gemini_client.max_tokens:
                self.gemini_client = GeminiClient(temperature=temperature, max_tokens=max_tokens)
            
            # Parse schema
            schema = self.schema_parser.parse_ddl(ddl_content)
            
            if not schema:
                raise ValueError("No tables found in DDL schema")
            
            # Get foreign key mapping
            fk_mapping = self.schema_parser.get_foreign_key_mapping()
            
            # For large datasets, generate in batches to avoid JSON issues
            # Smaller batch size = more reliable JSON parsing, fewer truncation errors
            batch_size = 15  # Generate max 15 rows per batch
            
            if num_rows > batch_size:
                # Generate in batches
                generated_data = self._generate_in_batches(
                    schema=schema,
                    instructions=instructions,
                    num_rows=num_rows,
                    foreign_key_mapping=fk_mapping,
                    batch_size=batch_size
                )
            else:
                # Generate all at once for small datasets
                generated_data = self.gemini_client.generate_synthetic_data(
                    schema=schema,
                    instructions=instructions,
                    num_rows=num_rows,
                    foreign_key_mapping=fk_mapping
                )
                logger.log_llm_call(
                  prompt=instructions,
                  response=f"Generated {num_rows} rows",
                  model="gemini-2.5-flash",
                   metadata={
                    "feature": "Synthetic Data",
                    "tables": list(schema.keys()),
                    "rows": num_rows
                  }
               )
            
            # Convert to DataFrames and validate
            dataframes = {}
            for table_name, records in generated_data.items():
                if records:
                    df = pd.DataFrame(records)
                    
                    # Validate data completeness
                    self._validate_generated_data(table_name, df, schema)
                    
                    dataframes[table_name] = df
            
            # Save to database
            self._save_to_database(dataframes, ddl_content)
            
            return dataframes
            
        except Exception as e:
            error_msg = f"Error generating data: {e}"
            logger.log_error(error_msg)
            raise
    
    def _generate_in_batches(
        self,
        schema: Dict[str, Any],
        instructions: str,
        num_rows: int,
        foreign_key_mapping: Dict[str, Any],
        batch_size: int = 15
    ) -> Dict[str, list]:
        """
        Generate data in batches to avoid JSON parsing issues with large datasets.
        
        Args:
            schema: Parsed schema dictionary
            instructions: User instructions
            num_rows: Total rows to generate
            foreign_key_mapping: FK relationships
            batch_size: Rows per batch
            
        Returns:
            Dictionary with table names as keys and lists of records as values
        """
        all_data = {}
        num_batches = (num_rows + batch_size - 1) // batch_size  # Ceiling division
        
        for batch_num in range(num_batches):
            batch_start = batch_num * batch_size
            batch_end = min((batch_num + 1) * batch_size, num_rows)
            batch_rows = batch_end - batch_start

            # Generate batch
            batch_instructions = f"{instructions}\nGenerate rows {batch_start + 1} to {batch_end}."

            try:
                batch_data = self.gemini_client.generate_synthetic_data(
                    schema=schema,
                    instructions=batch_instructions,
                    num_rows=batch_rows,
                    foreign_key_mapping=foreign_key_mapping
                )
            except Exception as e:
                # On a transient (504 timeout) failure with already-small batches we have
                # nothing left to shrink — surface a clearer error.
                if _is_transient_error(e) and batch_rows > 3:
                    logger.log_error(
                        f"Batch {batch_num + 1}/{num_batches} timed out at {batch_rows} rows. "
                        f"Splitting into smaller sub-batches and retrying."
                    )
                    batch_data = self._generate_in_batches(
                        schema=schema,
                        instructions=instructions,
                        num_rows=batch_rows,
                        foreign_key_mapping=foreign_key_mapping,
                        batch_size=max(3, batch_rows // 2),
                    )
                elif _is_transient_error(e):
                    raise RuntimeError(
                        "Gemini API timed out (504) even after retries and shrinking batches. "
                        "The schema may be too complex, or the API may be temporarily degraded. "
                        "Try again in a moment, reduce the number of rows, or simplify the schema."
                    ) from e
                else:
                    raise

            # Merge batch data into all_data
            for table_name, records in batch_data.items():
                if table_name not in all_data:
                    all_data[table_name] = []
                all_data[table_name].extend(records)

        return all_data
    
    def modify_table(
        self,
        table_name: str,
        modification_instruction: str,
        current_data: Optional[list] = None,
        schema_info: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        """
        Modify existing table data.
        
        Args:
            table_name: Name of the table to modify
            modification_instruction: User's modification instruction
            current_data: Current table data as list of dicts (if None, fetches from DB)
            schema_info: Table schema info (if None, fetches from DB)
            
        Returns:
            Modified DataFrame
        """
        try:
            # Get current table data if not provided
            if current_data is None:
                current_df = db_manager.get_table_data(table_name, limit=10000)
                current_data = current_df.to_dict('records')
            
            # Get table schema if not provided
            if schema_info is None:
                schema_info = db_manager.get_table_schema(table_name)
            
            # Generate modified data
            modified_data = self.gemini_client.modify_table_data(
                table_name=table_name,
                current_data=current_data,
                modification_instruction=modification_instruction,
                schema=schema_info
            )
            
            # Convert to DataFrame
            modified_df = pd.DataFrame(modified_data)
            
            return modified_df
            
        except Exception as e:
            error_msg = f"Error modifying table: {e}"
            logger.log_error(error_msg)
            raise
    
    def _save_to_database(self, dataframes: Dict[str, pd.DataFrame], ddl_content: str):
        """
        Save DataFrames to database.
        Uses 'replace' mode to drop and recreate tables, avoiding UNIQUE constraint issues.
        
        Args:
            dataframes: Dictionary of table names to DataFrames
            ddl_content: DDL content to create tables
        """
        try:
            # Insert data in order respecting foreign keys
            # Use 'replace' mode to drop and recreate tables (this avoids UNIQUE constraint issues)
            inserted_tables = set()
            max_iterations = len(dataframes) * 2  # Safety limit
            
            for _ in range(max_iterations):
                if len(inserted_tables) == len(dataframes):
                    break
                
                for table_name, df in dataframes.items():
                    if table_name in inserted_tables:
                        continue
                    
                    # Check if all foreign key dependencies are satisfied
                    schema = self.schema_parser.tables.get(table_name, {})
                    fks = schema.get("foreign_keys", [])
                    
                    can_insert = True
                    for fk in fks:
                        ref_table = fk["references_table"]
                        if ref_table not in inserted_tables and ref_table in dataframes:
                            can_insert = False
                            break
                    
                    if can_insert:
                        # Use 'replace' to drop and recreate table
                        # This avoids UNIQUE constraint failures from previous data
                        db_manager.insert_dataframe(table_name, df, if_exists="replace")
                        inserted_tables.add(table_name)
                        logger.log_event(
                         name="Database Insert",
                         metadata={
                          "table": table_name,
                          "rows": len(df)
                         }
                    )
            
            # Insert any remaining tables (might have circular dependencies)
            for table_name, df in dataframes.items():
                if table_name not in inserted_tables:
                    db_manager.insert_dataframe(table_name, df, if_exists="replace")
                    logger.log_llm_call(
                        prompt="",
                        model="gemini-2.5-flash",
                        response=f"Inserted {len(df)} rows into {table_name} (circular dependency)",
                        metadata={"table": table_name, "rows": len(df)}
                    )
                    
        except Exception as e:
            error_msg = f"Error saving to database: {e}"
            logger.log_error(error_msg)
            raise
    
    def _validate_generated_data(
        self,
        table_name: str,
        df: pd.DataFrame,
        schema: Dict[str, Any]
    ):
        """
        Validate that generated data includes all required columns and respects constraints.
        
        Args:
            table_name: Name of the table
            df: Generated DataFrame
            schema: Parsed schema dictionary
            
        Raises:
            ValueError: If validation fails
        """
        if table_name not in schema:
            return  # Skip validation if table not in schema
        
        table_schema = schema[table_name]
        schema_columns = {col["name"]: col for col in table_schema.get("columns", [])}
        df_columns = set(df.columns)
        
        # Check for missing columns
        missing_columns = set(schema_columns.keys()) - df_columns
        if missing_columns:
            # Try to add missing columns with default values
            for col_name in missing_columns:
                col_info = schema_columns[col_name]
                
                # If column is NOT NULL, this is an error
                if not col_info.get("nullable", True):
                    error_msg = (
                        f"Missing required NOT NULL column '{col_name}' in table '{table_name}'. "
                        f"Generated columns: {list(df_columns)}. "
                        f"Expected columns: {list(schema_columns.keys())}"
                    )
                    raise ValueError(error_msg)
                
                # For nullable columns, add with None
                df[col_name] = None
        
        # Check for NULL values in NOT NULL columns
        for col_name, col_info in schema_columns.items():
            if col_name in df.columns:
                if not col_info.get("nullable", True):
                    # Column is NOT NULL
                    null_count = df[col_name].isna().sum()
                    if null_count > 0:
                        raise ValueError(
                            f"Column '{col_name}' in table '{table_name}' is NOT NULL but has {null_count} null values"
                        )
        
        # Reorder columns to match schema
        ordered_columns = [col for col in schema_columns.keys() if col in df.columns]
        df = df[ordered_columns]

