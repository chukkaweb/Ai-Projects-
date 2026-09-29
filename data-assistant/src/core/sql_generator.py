"""
SQL generation from natural language queries.
"""

from typing import Dict, Any, Tuple
from llm.gemini_client import GeminiClient
from core.db import db_manager
from observability.langfuse_tracing import logger
from security.guardrails import validate_generated_sql,enforce_limit


class SQLGenerator:
    """Generates SQL queries from natural language."""
    
    def __init__(self):
        """Initialize SQL generator."""
        self.gemini_client = GeminiClient(temperature=0.1)
    
    def generate_and_execute(
        self,
        natural_language_query: str
    ) -> Tuple[str, Any]:
        """
        Generate SQL from natural language and execute it.
        
        Args:
            natural_language_query: User's natural language question
            
        Returns:
            Tuple of (SQL query, results DataFrame)
        """
        try:
            logger.log_user_query(natural_language_query, "nl_query")
            
            # Get schema metadata
            schema_metadata = db_manager.get_all_schemas()
            
            if not schema_metadata:
                raise ValueError("No tables found in database. Please generate data first.")
            
            # Generate SQL
            sql_query = self.gemini_client.generate_sql(
                natural_language_query=natural_language_query,
                schema_metadata=schema_metadata
            )
            
            # Guardrails 
            if not validate_generated_sql(sql_query):
                  raise ValueError(
                  "Unsafe SQL query blocked."
            )
            sql_query = enforce_limit(sql_query)
            
            # Execute SQL (only SELECT queries for safety)
            if not sql_query.strip().upper().startswith('SELECT'):
                raise ValueError("Only SELECT queries are allowed for safety.")
            
            # Execute query
            results_df = db_manager.execute_query(sql_query)
            
            return sql_query, results_df
            
        except Exception as e:
            error_msg = f"Error generating/executing SQL: {e}"
            logger.log_error(error_msg)
            raise

