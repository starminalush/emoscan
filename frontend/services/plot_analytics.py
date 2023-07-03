import pandas as pd
from plotly import graph_objects as go

from data_classes import Analytics


def plot_analytics(analytics: list[Analytics]) -> go.Figure:
    """Plot analytics graph of recognition emotions by range of dates.

    Args:
        analytics: List of dicts each containing emotion, total number of emotions over range of dates and track_id.

    Returns:
        Plotly Figure object.
    """
    df = pd.DataFrame(analytics)
    grouped_data = df.groupby("emotion")
    fig = go.Figure()
    for emotion, emotion_data in grouped_data:
        fig.add_trace(
            go.Scatter(
                x=emotion_data["date"],
                y=emotion_data["count"],
                mode="lines+markers",
                name=emotion,
            )
        )
    return fig
