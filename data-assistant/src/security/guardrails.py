import re
from llm.gemini_client import GeminiClient

gemini = GeminiClient()

INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "forget instructions",
    "system prompt",
    "developer prompt",
    "reveal prompt",
    "show hidden prompt",
    "bypass security",
    "jailbreak",
    "act as root",
    "act as system",
    "print api key",
    "show credentials"
]

ALLOWED_KEYWORDS = [
    "sql",
    "database",
    "table",
    "schema",
    "company"
    "city"
    "employee",
    "department",
    "locations"
    "customer",
    "restaurant",
    "query",
    "data",
    "sales",
    "chart",
    "plot",
    "analytics"
]

BLOCKED_SQL_WORDS = [
    "drop",
    "delete",
    "truncate",
    "alter",
    "grant",
    "revoke",
    "update",
    "insert"
]

# -------------------------
# Prompt Injection Detection
# -------------------------

def detect_prompt_injection(user_input: str):

    text = user_input.lower()

    for pattern in INJECTION_PATTERNS:
        if pattern in text:
            return True

    return False

# -------------------------
# Off Topic Detection
# -------------------------
def is_on_topic(user_input: str):
   return gemini.is_query_on_topic(user_input)
# -------------------------
# PII Masking
# -------------------------
def mask_pii(text: str):

    # Email
    text = re.sub(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        '[EMAIL]',
        text
    )

    # Phone
    text = re.sub(
        r'\b\d{10}\b',
        '[PHONE]',
        text
    )

    return text

# -------------------------
# SQL Protection
# -------------------------
def validate_generated_sql(sql_query):
    sql_lower = sql_query.lower()
    for word in BLOCKED_SQL_WORDS:
        if word in sql_query:
         return False
    return True

def enforce_limit(sql):

    if "limit" not in sql.lower():
        sql = sql.rstrip(";")
        sql += " LIMIT 100"

    return sql
