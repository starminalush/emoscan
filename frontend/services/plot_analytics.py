import pandas as pd
import plotly.graph_objects as go


def plot_analytics(analytics: list):
    df = pd.DataFrame(analytics)

    # Группировка данных по полю 'emotion'
    grouped_data = df.groupby("emotion")

    # Создание графиков для каждой эмоции
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
