import streamlit as st
import pandas as pd
import os
import sys

app_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(app_dir, '../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if os.path.join(root_dir, 'app') not in sys.path:
    sys.path.insert(0, os.path.join(root_dir, 'app'))

from src.db_manager import DBManager
try:
    from components.charts import create_donut_chart, create_bar_chart
except Exception:
    from app.components.charts import create_donut_chart, create_bar_chart

def render_marketing_page():
    st.markdown("### 📈 Module 7: Marketing Channel Analytics & Lead Source ROI")

    leads_df = DBManager.get_table_df("leads")

    if leads_df.empty:
        st.info("📂 No lead records available in database.")
        return

    st.subheader("📢 Channel-wise Lead Share Volume")
    source_dist = leads_df.groupby('lead_source')['lead_id'].count().reset_index()
    source_dist.columns = ['lead_source', 'lead_count']

    col1, col2 = st.columns([1, 1])

    with col1:
        fig_donut = create_donut_chart(source_dist, names_col='lead_source', values_col='lead_count', title="Lead Volume per Channel")
        st.plotly_chart(fig_donut, use_container_width=True)

    with col2:
        st.subheader("🎯 Channel Conversion Rate %")
        conv_df = leads_df[leads_df['status'] == 'Converted Admission'].groupby('lead_source')['lead_id'].count().reset_index()
        conv_df.columns = ['lead_source', 'converted_count']

        merged = pd.merge(source_dist, conv_df, on='lead_source', how='left').fillna(0)
        merged['Conversion_Pct'] = round((merged['converted_count'] / merged['lead_count']) * 100.0, 1)

        fig_bar = create_bar_chart(merged, x_col='lead_source', y_col='Conversion_Pct', title="Admissions Conversion Rate (%)")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Marketing Channel Performance Matrix")
    st.dataframe(merged, use_container_width=True)

if __name__ == '__main__':
    render_marketing_page()
