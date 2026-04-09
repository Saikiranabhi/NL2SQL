def validate_sql(sql: str) -> bool:
    """
    Validates SQL query to ensure it's safe to execute.
    Only allows SELECT queries.
    """

    if not sql:
        raise ValueError("SQL query is empty")

    sql_lower = sql.lower().strip()

    # Allow only SELECT queries
    if not sql_lower.startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    # Block dangerous keywords
    forbidden_keywords = [
        "insert", "update", "delete", "drop", "alter",
        "exec", "grant", "revoke", "shutdown"
    ]

    for keyword in forbidden_keywords:
        if keyword in sql_lower:
            raise ValueError(f"Forbidden keyword detected: {keyword}")

    # Block system tables
    if "sqlite_master" in sql_lower:
        raise ValueError("Access to system tables is not allowed")

    return True