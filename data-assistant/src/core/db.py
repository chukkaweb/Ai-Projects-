"""
Database connection and operations module using SQLAlchemy with SQLite.
SQLite is lightweight and requires no external database installation.
"""

import os
import re
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from dotenv import load_dotenv
from observability.langfuse_tracing import logger

load_dotenv()


class DatabaseManager:
    """Manages SQLite database connections and operations."""
    
    def __init__(self):
        """Initialize database connection (lazy connection)."""
        # Use SQLite database stored in project root
        db_path = os.getenv("DATABASE_PATH", "synthetic_data.db")
        
        # Ensure absolute path
        if not os.path.isabs(db_path):
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(project_root, db_path)
        
        self.db_path = db_path
        self.connection_string = f"sqlite:///{db_path}"
        
        self.engine: Optional[Engine] = None
        self._connected = False
        
        logger.log_llm_call(
            prompt="",
            model="gemini-2.5-flash",
            response=f"Database initialized at: {self.db_path}",
            metadata={"database": "SQLite", "path": db_path}
        )
    
    def _connect(self):
        """Create database connection (lazy connection)."""
        if self._connected and self.engine is not None:
            return
        
        try:
            self.engine = create_engine(
                self.connection_string,
                pool_pre_ping=True,
                echo=False
            )
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            self._connected = True
            logger.log_llm_call(
                prompt="",
                model="gemini-2.5-flash",
                response="Database connection established",
                metadata={"status": "connected"}
            )
        except Exception as e:
            self._connected = False
            logger.log_error(f"Database connection error: {e}")
            # Don't raise - allow app to start without DB
    
    def _ensure_connected(self):
        """Ensure database connection is established."""
        if not self._connected:
            self._connect()
        if not self._connected or self.engine is None:
            raise ConnectionError(
                f"Database connection failed. Please check: {self.db_path}"
            )
    
    def execute_ddl(self, ddl_statements: str, add_if_not_exists: bool = True):
        """
        Execute DDL statements to create tables.
        Each statement is executed in its own transaction.
        
        Args:
            ddl_statements: SQL DDL statements
            add_if_not_exists: If True, add IF NOT EXISTS to CREATE TABLE statements
        """
        self._ensure_connected()
        
        # SQLite-specific adjustments
        ddl_statements = self._convert_ddl_to_sqlite(ddl_statements)
        
        # Split by semicolon and execute each statement
        statements = [s.strip() for s in ddl_statements.split(';') if s.strip()]
        
        for statement in statements:
            if not statement:
                continue
            
            # Add IF NOT EXISTS to CREATE TABLE statements if not present
            if add_if_not_exists and statement.upper().startswith('CREATE TABLE'):
                if 'IF NOT EXISTS' not in statement.upper():
                    statement = re.sub(
                        r'CREATE TABLE\s+',
                        'CREATE TABLE IF NOT EXISTS ',
                        statement,
                        flags=re.IGNORECASE
                    )
            
            # Execute each statement in its own transaction
            try:
                with self.engine.begin() as conn:
                    conn.execute(text(statement))
            except SQLAlchemyError as e:
                error_str = str(e).lower()
                if 'already exists' in error_str or 'duplicate' in error_str:
                    continue
                else:
                    logger.log_error(f"DDL execution error: {statement[:100]}... Error: {e}")
                    continue
    
    def _convert_ddl_to_sqlite(self, ddl: str) -> str:
        """
        Convert PostgreSQL DDL to SQLite-compatible DDL.
        
        Args:
            ddl: PostgreSQL DDL statements
            
        Returns:
            SQLite-compatible DDL statements
        """
        # Convert PostgreSQL data types to SQLite equivalents
        conversions = {
            r'\bSERIAL\b': 'INTEGER',
            r'\bBIGSERIAL\b': 'INTEGER',
            r'\bVARCHAR': 'TEXT',
            r'\bCHAR': 'TEXT',
            r'\bTEXT\b': 'TEXT',
            r'\bBOOLEAN\b': 'INTEGER',
            r'\bTIMESTAMP\b': 'TEXT',
            r'\bDATE\b': 'TEXT',
            r'\bTIME\b': 'TEXT',
            r'\bDECIMAL': 'REAL',
            r'\bNUMERIC': 'REAL',
            r'\bDOUBLE PRECISION\b': 'REAL',
        }
        
        result = ddl
        for pattern, replacement in conversions.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    def insert_dataframe(self, table_name: str, df: pd.DataFrame, if_exists: str = "replace"):
        """
        Insert DataFrame into SQLite table.
        
        Args:
            table_name: Name of the table
            df: DataFrame to insert
            if_exists: What to do if table exists ('replace', 'append', 'fail')
        """
        self._ensure_connected()
        try:
            df.to_sql(
                table_name,
                self.engine,
                if_exists=if_exists,
                index=False,
                method='multi'
            )
        except SQLAlchemyError as e:
            logger.log_error(f"DataFrame insert error: {e}")
            raise
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute a SELECT query and return results as DataFrame.
        
        Args:
            query: SQL query string
            
        Returns:
            DataFrame with query results
        """
        self._ensure_connected()
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                return df
        except SQLAlchemyError as e:
            logger.log_error(f"Query execution error: {e}")
            raise
    
    def get_table_names(self) -> List[str]:
        """
        Get list of all table names in the database.
        
        Returns:
            List of table names
        """
        self._ensure_connected()
        try:
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        except Exception as e:
            logger.log_error(f"Error getting table names: {e}")
            return []
    
    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """
        Get schema information for a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary with column information
        """
        self._ensure_connected()
        try:
            inspector = inspect(self.engine)
            columns = inspector.get_columns(table_name)
            return {
                "columns": [
                    {
                        "name": col["name"],
                        "type": str(col["type"]),
                        "nullable": col["nullable"]
                    }
                    for col in columns
                ],
                "primary_keys": inspector.get_pk_constraint(table_name).get("constrained_columns", []),
                "foreign_keys": [
                    {
                        "column": fk["constrained_columns"][0] if fk["constrained_columns"] else None,
                        "referred_table": fk["referred_table"],
                        "referred_column": fk["referred_columns"][0] if fk["referred_columns"] else None
                    }
                    for fk in inspector.get_foreign_keys(table_name)
                ]
            }
        except Exception as e:
            logger.log_error(f"Error getting table schema: {e}")
            return {}
    
    def get_all_schemas(self) -> Dict[str, Dict[str, Any]]:
        """
        Get schema information for all tables.
        
        Returns:
            Dictionary mapping table names to their schemas
        """
        self._ensure_connected()
        schemas = {}
        for table_name in self.get_table_names():
            schemas[table_name] = self.get_table_schema(table_name)
        return schemas
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists.
        
        Args:
            table_name: Name of the table
            
        Returns:
            True if table exists, False otherwise
        """
        self._ensure_connected()
        return table_name in self.get_table_names()
    
    def get_table_data(self, table_name: str, limit: int = 100) -> pd.DataFrame:
        """
        Get data from a table.
        
        Args:
            table_name: Name of the table
            limit: Maximum number of rows to return
            
        Returns:
            DataFrame with table data
        """
        self._ensure_connected()
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        return self.execute_query(query)
    
    def truncate_all_tables(self, restart_identity: bool = True, cascade: bool = True):
        """
        Safely truncate all tables in the database.
        SQLite doesn't support TRUNCATE, so we use DELETE.
        
        Args:
            restart_identity: If True, reset auto-increment sequences (ignored in SQLite)
            cascade: If True, delete from dependent tables (handled automatically)
        
        Returns:
            List of truncated table names
        """
        self._ensure_connected()
        
        try:
            table_names = self.get_table_names()
            
            if not table_names:
                return []
            
            # SQLite doesn't support TRUNCATE, use DELETE instead
            truncated_tables = []
            
            for table_name in table_names:
                try:
                    with self.engine.begin() as conn:
                        # Delete all rows
                        conn.execute(text(f'DELETE FROM "{table_name}"'))
                        
                        # Reset SQLite auto-increment if restart_identity is True
                        if restart_identity:
                            conn.execute(text(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'"))
                        
                        truncated_tables.append(table_name)
                except Exception as e:
                    logger.log_error(f"Error truncating {table_name}: {e}")
                    continue
            
            return truncated_tables
                
        except Exception as e:
            error_msg = f"Error truncating tables: {e}"
            logger.log_error(error_msg)
            raise
    
    def _get_table_dependencies(self) -> Dict[str, List[str]]:
        """
        Get foreign key dependencies for all tables.
        
        Returns:
            Dictionary mapping table names to lists of tables they depend on
        """
        self._ensure_connected()
        dependencies = {}
        
        try:
            inspector = inspect(self.engine)
            all_tables = inspector.get_table_names()
            
            for table_name in all_tables:
                fks = inspector.get_foreign_keys(table_name)
                deps = [fk["referred_table"] for fk in fks]
                dependencies[table_name] = deps
                
        except Exception as e:
            logger.log_error(f"Error getting table dependencies: {e}")
        
        return dependencies
    
    def _sort_tables_by_dependencies(
        self, 
        table_names: List[str], 
        dependencies: Dict[str, List[str]]
    ) -> List[str]:
        """
        Sort tables by dependency order (tables with no dependencies first).
        
        Args:
            table_names: List of table names to sort
            dependencies: Dictionary of table dependencies
            
        Returns:
            Sorted list of table names
        """
        sorted_tables = []
        remaining = set(table_names)
        
        while remaining:
            ready = [
                table for table in remaining
                if not any(dep in remaining for dep in dependencies.get(table, []))
            ]
            
            if not ready:
                sorted_tables.extend(remaining)
                break
            
            sorted_tables.extend(ready)
            remaining -= set(ready)
        
        return sorted_tables


# Global database manager instance
db_manager = DatabaseManager()
