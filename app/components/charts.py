import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# High-Contrast Executive Light Layout
LIGHT_LAYOUT = dict(
    paper_bgcolor='#ffffff',
    plot_bgcolor='#ffffff',
    font=dict(color='#0f172a', family='Inter, Segoe UI, sans-serif', size=12),
    margin=dict(l=25, r=25, t=45, b=25),
    legend=dict(font=dict(color='#0f172a', size=11), bgcolor='#ffffff'),
    xaxis=dict(gridcolor='#f1f5f9', tickfont=dict(color='#334155', size=10)),
    yaxis=dict(gridcolor='#f1f5f9', tickfont=dict(color='#334155', size=10)),
)

def create_bar_chart(df, x_col, y_col, title="Bar Chart", color_col=None):
    if df is None or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No Data Available", showarrow=False, font=dict(size=18, color="#64748b"))
        fig.update_layout(**LIGHT_LAYOUT)
        return fig

    fig = px.bar(
        df, x=x_col, y=y_col, color=color_col if color_col in df.columns else None,
        title=title, text_auto='.2s',
        color_discrete_sequence=['#059669', '#0284c7', '#8b5cf6', '#f59e0b', '#ec4899', '#10b981']
    )
    fig.update_layout(**LIGHT_LAYOUT)
    fig.update_traces(marker_line_color='#0284c7', marker_line_width=1, opacity=0.9)
    return fig

def create_line_chart(df, x_col, y_col, title="Trend Chart"):
    if df is None or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No Data Available", showarrow=False, font=dict(size=18, color="#64748b"))
        fig.update_layout(**LIGHT_LAYOUT)
        return fig

    fig = px.line(
        df, x=x_col, y=y_col, title=title, markers=True,
        color_discrete_sequence=['#059669']
    )
    fig.update_layout(**LIGHT_LAYOUT)
    fig.update_traces(line=dict(width=3, color='#059669'), marker=dict(size=8, color='#0284c7'))
    return fig

def create_donut_chart(df, names_col, values_col, title="Distribution"):
    if df is None or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No Data Available", showarrow=False, font=dict(size=18, color="#64748b"))
        fig.update_layout(**LIGHT_LAYOUT)
        return fig

    fig = px.pie(
        df, names=names_col, values=values_col, title=title, hole=0.45,
        color_discrete_sequence=['#059669', '#0284c7', '#8b5cf6', '#f59e0b', '#ec4899', '#38bdf8']
    )
    fig.update_layout(**LIGHT_LAYOUT)
    fig.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='#ffffff', size=11, family='sans-serif'))
    return fig

def create_gauge_chart(value, title="Target Progress", target=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 16, 'color': '#047857'}},
        delta={'reference': target, 'increasing': {'color': "#059669"}},
        gauge={
            'axis': {'range': [None, max(target, value * 1.2)], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': "#059669"},
            'bgcolor': "#ffffff",
            'borderwidth': 1,
            'bordercolor': "#cbd5e1",
            'steps': [
                {'range': [0, target * 0.5], 'color': '#fee2e2'},
                {'range': [target * 0.5, target * 0.85], 'color': '#fef3c7'},
                {'range': [target * 0.85, target * 1.2], 'color': '#d1fae5'}
            ],
        }
    ))
    fig.update_layout(**LIGHT_LAYOUT)
    return fig