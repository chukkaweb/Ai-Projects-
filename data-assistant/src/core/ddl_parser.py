"""
SQL DDL schema parser to extract table structures, columns, constraints.
"""

import re
from typing import Dict, List, Any, Optional


class SchemaParser:
    """Parses SQL DDL statements to extract schema information."""
    
    def __init__(self):
        """Initialize schema parser."""
        self.tables: Dict[str, Dict[str, Any]] = {}
    
    def parse_ddl(self, ddl_content: str) -> Dict[str, Dict[str, Any]]:
        """
        Parse DDL content and extract schema information.
        
        Args:
            ddl_content: SQL DDL statements as string
            
        Returns:
            Dictionary with table names as keys and schema info as values
        """
        self.tables = {}
        
        # Normalize DDL content
        ddl_content = self._normalize_ddl(ddl_content)
        
        # Extract CREATE TABLE statements
        # Use a more robust pattern that handles nested parentheses
        create_table_pattern = r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?["\']?(\w+)["\']?\s*\(((?:[^()]|\([^()]*\))*)\);?'
        matches = re.finditer(create_table_pattern, ddl_content, re.IGNORECASE)
        
        for match in matches:
            table_name = match.group(1).lower()
            table_body = match.group(2)
            
            table_info = self._parse_table_body(table_name, table_body)
            self.tables[table_name] = table_info
        
        return self.tables
    
    def _normalize_ddl(self, ddl_content: str) -> str:
        """
        Normalize DDL content for easier parsing.
        
        Args:
            ddl_content: Raw DDL content
            
        Returns:
            Normalized DDL content
        """
        # Remove comments
        ddl_content = re.sub(r'--.*?$', '', ddl_content, flags=re.MULTILINE)
        ddl_content = re.sub(r'/\*.*?\*/', '', ddl_content, flags=re.DOTALL)
        
        # Normalize whitespace
        ddl_content = re.sub(r'\s+', ' ', ddl_content)
        
        return ddl_content
    
    def _parse_table_body(self, table_name: str, table_body: str) -> Dict[str, Any]:
        """
        Parse table body to extract columns, constraints, etc.
        
        Args:
            table_name: Name of the table
            table_body: Body of CREATE TABLE statement
            
        Returns:
            Dictionary with table schema information
        """
        columns = []
        primary_keys = []
        foreign_keys = []
        
        # Split by comma, but handle nested parentheses
        parts = self._split_by_comma_respecting_parens(table_body)
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # Check for PRIMARY KEY constraint
            if re.match(r'PRIMARY\s+KEY', part, re.IGNORECASE):
                pk_match = re.search(r'\(([^)]+)\)', part)
                if pk_match:
                    pk_cols = [c.strip().strip('"\'') for c in pk_match.group(1).split(',')]
                    primary_keys.extend(pk_cols)
            
            # Check for FOREIGN KEY constraint
            elif re.match(r'FOREIGN\s+KEY', part, re.IGNORECASE):
                fk_match = re.search(
                    r'FOREIGN\s+KEY\s*\(([^)]+)\)\s*REFERENCES\s+(\w+)\s*\(([^)]+)\)',
                    part,
                    re.IGNORECASE
                )
                if fk_match:
                    foreign_keys.append({
                        "column": fk_match.group(1).strip().strip('"\''),
                        "references_table": fk_match.group(2).lower().strip(),
                        "references_column": fk_match.group(3).strip().strip('"\'')
                    })
            
            # Regular column definition
            else:
                col_info = self._parse_column(part)
                if col_info:
                    columns.append(col_info)
        
        return {
            "name": table_name,
            "columns": columns,
            "primary_keys": primary_keys,
            "foreign_keys": foreign_keys
        }
    
    def _parse_column(self, column_def: str) -> Optional[Dict[str, Any]]:
        """
        Parse a single column definition with proper NOT NULL detection.
        
        Args:
            column_def: Column definition string
            
        Returns:
            Dictionary with column information or None
        """
        # Clean up the column definition
        column_def = column_def.strip()
        
        # Extract column name (handle quoted names and spaces)
        name_match = re.match(r'["\']?(\w+)["\']?\s+', column_def)
        if not name_match:
            return None
        
        column_name = name_match.group(1).lower()
        
        # Extract data type (including SERIAL)
        type_pattern = r'\b(SERIAL|BIGSERIAL|VARCHAR|CHAR|TEXT|INTEGER|INT|BIGINT|SMALLINT|DECIMAL|NUMERIC|REAL|DOUBLE\s+PRECISION|FLOAT|BOOLEAN|BOOL|DATE|TIME|TIMESTAMP(?:TZ)?|UUID|JSON|JSONB)\b'
        type_match = re.search(type_pattern, column_def, re.IGNORECASE)
        data_type = type_match.group(1).upper().replace(' ', '_') if type_match else "TEXT"
        
        # Extract size if present (e.g., VARCHAR(255), DECIMAL(10,2))
        size_match = re.search(r'\(([^)]+)\)', column_def)
        size = size_match.group(1) if size_match else None
        
        # Check for NOT NULL - be very explicit
        # Remove the data type and size first to avoid false matches
        constraint_part = column_def
        if type_match:
            constraint_part = column_def[type_match.end():]
        if size_match:
            constraint_part = constraint_part.replace(size_match.group(0), '')
        
        # Now check for NOT NULL in the constraints part
        not_null = bool(re.search(r'\bNOT\s+NULL\b', constraint_part, re.IGNORECASE))
        
        # Check for UNIQUE
        unique = bool(re.search(r'\bUNIQUE\b', constraint_part, re.IGNORECASE))
        
        # Check for PRIMARY KEY (implies NOT NULL)
        is_primary = bool(re.search(r'\bPRIMARY\s+KEY\b', constraint_part, re.IGNORECASE))
        if is_primary:
            not_null = True
        
        # Check for DEFAULT
        default_match = re.search(r'DEFAULT\s+([^,]+?)(?:\s*,|\s*$)', constraint_part, re.IGNORECASE)
        default_value = default_match.group(1).strip() if default_match else None
        
        # SERIAL columns are auto-increment and typically NOT NULL
        if data_type in ('SERIAL', 'BIGSERIAL'):
            not_null = True
        
        return {
            "name": column_name,
            "type": data_type,
            "size": size,
            "nullable": not not_null,  # nullable is opposite of not_null
            "unique": unique,
            "default": default_value,
            "is_primary": is_primary
        }
    
    def _split_by_comma_respecting_parens(self, text: str) -> List[str]:
        """
        Split text by comma while respecting parentheses.
        
        Args:
            text: Text to split
            
        Returns:
            List of split parts
        """
        parts = []
        current = ""
        depth = 0
        
        for char in text:
            if char == '(':
                depth += 1
                current += char
            elif char == ')':
                depth -= 1
                current += char
            elif char == ',' and depth == 0:
                parts.append(current.strip())
                current = ""
            else:
                current += char
        
        if current.strip():
            parts.append(current.strip())
        
        return parts
    
    def get_foreign_key_mapping(self) -> Dict[str, Any]:
        """
        Get foreign key relationships mapping.
        
        Returns:
            Dictionary mapping foreign keys to their references
        """
        fk_mapping = {}
        
        for table_name, table_info in self.tables.items():
            for fk in table_info.get("foreign_keys", []):
                fk_key = f"{table_name}.{fk['column']}"
                fk_mapping[fk_key] = {
                    "references_table": fk["references_table"],
                    "references_column": fk["references_column"]
                }
        
        return fk_mapping
    
    def get_schema_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the parsed schema.
        
        Returns:
            Dictionary with schema summary
        """
        summary = {
            "tables": {},
            "foreign_keys": self.get_foreign_key_mapping()
        }
        
        for table_name, table_info in self.tables.items():
            summary["tables"][table_name] = {
                "columns": [col["name"] for col in table_info["columns"]],
                "primary_keys": table_info["primary_keys"],
                "foreign_keys": [
                    f"{fk['column']} -> {fk['references_table']}.{fk['references_column']}"
                    for fk in table_info["foreign_keys"]
                ]
            }
        
        return summary

