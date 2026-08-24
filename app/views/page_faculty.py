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
    from components.charts import create_bar_chart
except Exception:
    from app.components.charts import create_bar_chart

def render_faculty_page():
    st.markdown("### 👨‍🏫 Module 8: Faculty Performance Analytics & Student Ratings")

    batches_df = DBManager.get_table_df("batches")
    feedbacks_df = DBManager.get_table_df("feedbacks")

    if batches_df.empty:
        st.info("📂 No faculty batch records available.")
        return

    st.subheader("📊 Faculty Workload & Batch Count")
    fac_summary = batches_df.groupby('faculty_name')['batch_name'].count().reset_index()
    fac_summary.columns = ['faculty_name', 'total_batches']

    col1, col2 = st.columns([1, 1])

    with col1:
        fig_bar = create_bar_chart(fac_summary, x_col='faculty_name', y_col='total_batches', title="Active Batches per Faculty")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("⭐ Faculty Student Ratings (Out of 5 Stars)")
        if not feedbacks_df.empty:
            avg_ratings = feedbacks_df.groupby('faculty_name')['rating'].mean().reset_index()
            avg_ratings['rating'] = round(avg_ratings['rating'], 2)
            fig_stars = create_bar_chart(avg_ratings, x_col='faculty_name', y_col='rating', title="Average Feedback Score (1 to 5 Stars)")
            st.plotly_chart(fig_stars, use_container_width=True)

    st.markdown("---")
    st.subheader("💬 Student Feedback & Sentiment Reviews")
    if not feedbacks_df.empty:
        st.dataframe(feedbacks_df, use_container_width=True)

if __name__ == '__main__':
    render_faculty_page()
