def format_response(sql: str, columns: list, rows: list, chart: dict = None):
    """
    Formats the final API response.
    """

    return {
        "message": "Query executed successfully",
        "sql_query": sql,
        "columns": columns,
        "rows": rows,
        "row_count": len(rows),
        "chart": chart if chart else {},
        "chart_type": "bar" if chart else None
    }


def format_error(error_message: str):
    """
    Standard error response
    """
    return {
        "message": "Error occurred",
        "error": error_message,
        "sql_query": None,
        "columns": [],
        "rows": [],
        "row_count": 0,
        "chart": {},
        "chart_type": None
    }