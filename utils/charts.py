import json
import plotly.express as px
import pandas as pd


def generate_chart(columns: list, rows: list):
    """
    Generates a simple chart from query results.
    Returns a JSON-serializable dict (not raw Plotly object).
    """

    if not columns or not rows or len(columns) < 2:
        return None

    try:
        df = pd.DataFrame(rows, columns=columns)

        x_col = columns[0]
        y_col = columns[1]

        fig = px.bar(df, x=x_col, y=y_col)

        # ✅ FIX: convert to JSON string then parse back to plain dict
        return json.loads(fig.to_json())

    except Exception:
        return None