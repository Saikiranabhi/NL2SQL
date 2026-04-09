import plotly.express as px
import pandas as pd


def generate_chart(columns: list, rows: list):
    """
    Generates a simple chart from query results.
    Assumes first column = x-axis, second column = y-axis.
    """

    if not columns or not rows or len(columns) < 2:
        return None

    try:
        df = pd.DataFrame(rows, columns=columns)

        x_col = columns[0]
        y_col = columns[1]

        fig = px.bar(df, x=x_col, y=y_col)

        return fig.to_dict()

    except Exception:
        return None