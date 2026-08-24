import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Dark Theme Palette
DARK_LAYOUT = dict(
    paper_bgcolor='rgba(15, 23, 42, 0.7)',
    plot_bgcolor='rgba(15, 23, 42, 0)',
    font=dict(color='#f8fafc', family='Calibri, sans-serif'),
    margin=dict(l=20, r=20, t=40, b=20),
)

def create_bar_chart(df, x_col, y_col, title="Bar Chart", color_col=None):
    if df is None or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No Data Available", showarrow=False, font=dict(size=18, color="gray"))
        fig.update_layout(**DARK_LAYOUT)
        return fig

    fig = px.bar(
        df, x=x_col, y=y_col, color=color_col if color_col in df.columns else None,
        title=title, text_auto='.2s',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_layout(**DARK_LAYOUT)
    fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.9)
    return fig

def create_line_chart(df, x_col, y_col, title="Trend Chart"):
    if df is None or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No Data Available", showarrow=False, font=dict(size=18, color="gray"))
        fig.update_layout(**DARK_LAYOUT)
        return fig

    fig = px.line(
        df, x=x_col, y=y_col, title=title, markers=True,
        color_discrete_sequence=['#10b981']
    )
    fig.update_layout(**DARK_LAYOUT)
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    return fig

def create_donut_chart(df, names_col, values_col, title="Distribution"):
    if df is None or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No Data Available", showarrow=False, font=dict(size=18, color="gray"))
        fig.update_layout(**DARK_LAYOUT)
        return fig

    fig = px.pie(
        df, names=names_col, values=values_col, title=title, hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig.update_layout(**DARK_LAYOUT)
    return fig

def create_gauge_chart(value, title="Target Progress", target=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 18, 'color': '#10b981'}},
        delta={'reference': target, 'increasing': {'color': "#10b981"}},
        gauge={
            'axis': {'range': [None, max(target, value * 1.2)], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#10b981"},
            'bgcolor': "rgba(30, 41, 59, 0.8)",
            'borderwidth': 2,
            'bordercolor': "#334155",
            'steps': [
                {'range': [0, target * 0.5], 'color': 'rgba(239, 68, 68, 0.3)'},
                {'range': [target * 0.5, target * 0.85], 'color': 'rgba(245, 158, 11, 0.3)'},
                {'range': [target * 0.85, target * 1.2], 'color': 'rgba(16, 185, 129, 0.3)'}
            ],
        }
    ))
    fig.update_layout(**DARK_LAYOUT)
    return fig