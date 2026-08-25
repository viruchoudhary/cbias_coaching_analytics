import streamlit as st
import pandas as pd
from datetime import datetime
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
    from components.charts import create_bar_chart, create_line_chart
except Exception:
    from app.components.charts import create_bar_chart, create_line_chart

def render_tests_page():
    st.markdown("### 🏆 Module 7: Test Creation & Academic Performance Portal")

    students_df = DBManager.get_table_df("students")
    batches_df = DBManager.get_table_df("batches")
    test_scores_df = DBManager.get_table_df("test_scores")

    # Build Composite Unique Student Options (ID + Name + Mobile + Batch)
    student_options = []
    student_map = {}
    if not students_df.empty:
        for idx, row in students_df.iterrows():
            s_id = row.get('id', idx + 1)
            name = row.get('full_name', 'Student')
            mob = row.get('parent_mobile', 'N/A')
            batch = row.get('batch_name', 'General')
            
            opt_str = f"ID: #{s_id} - {name} | Mob: {mob} | Batch: {batch}"
            student_options.append(opt_str)
            student_map[opt_str] = (name, s_id)
    else:
        opt_str = "ID: #1 - Aarav Sharma | Mob: 9876543210 | Batch: Batch-A"
        student_options = [opt_str]
        student_map[opt_str] = ("Aarav Sharma", 1)

    t1, t2 = st.columns(2)

    # 1. New Test Marks Entry Form
    with t1:
        with st.expander("➕ Record Student Test Marks", expanded=False):
            with st.form("new_test_score_form"):
                selected_option = st.selectbox("Select Student (Unique ID & Mobile) *", student_options)
                raw_name, selected_id = student_map.get(selected_option, ("Student", 1))

                test_name = st.text_input("Test / Exam Title *", value="Mid-Term Assessment")
                marks_obtained = st.number_input("Marks Obtained *", min_value=0.0, max_value=100.0, value=75.0, step=1.0)
                total_marks = st.number_input("Maximum Marks *", min_value=10.0, max_value=500.0, value=100.0, step=10.0)

                test_sub = st.form_submit_button("✅ Save Test Score")
                if test_sub and selected_option:
                    pct = round((marks_obtained / total_marks) * 100.0, 1)
                    grade = "A+" if pct >= 90 else ("A" if pct >= 75 else ("B" if pct >= 60 else "Fail"))

                    conn = DBManager.get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO test_scores (student_name, test_name, marks_obtained, total_marks, grade) VALUES (?, ?, ?, ?, ?)",
                        (f"{raw_name} (ID: #{selected_id})", test_name, marks_obtained, total_marks, grade)
                    )
                    conn.commit()
                    conn.close()
                    st.success(f"🎉 Test Score Saved for **{raw_name} (ID: #{selected_id})**: {marks_obtained}/{total_marks} ({pct}%, Grade: {grade})!")
                    st.rerun()

    # 2. Performance Summary Metrics
    with t2:
        if not test_scores_df.empty:
            avg_marks = round(test_scores_df['marks_obtained'].mean(), 1)
            high_marks = test_scores_df['marks_obtained'].max()
            low_marks = test_scores_df['marks_obtained'].min()

            mc1, mc2, mc3 = st.columns(3)
            mc1.metric("📊 Class Average", f"{avg_marks}/100")
            mc2.metric("🏆 Highest Score", f"{high_marks}/100")
            mc3.metric("⚠️ Lowest Score", f"{low_marks}/100")

    st.markdown("---")

    # 3. Master Test Scores Table & Performance Graph
    if not test_scores_df.empty:
        st.subheader("📈 Student Academic Marks Directory")
        st.dataframe(test_scores_df, use_container_width=True)

        st.subheader("📊 Student Test Performance Distribution")
        fig_bar = create_bar_chart(test_scores_df, x_col='student_name', y_col='marks_obtained', title="Marks Obtained per Student")
        st.plotly_chart(fig_bar, use_container_width=True)

if __name__ == '__main__':
    render_tests_page()
