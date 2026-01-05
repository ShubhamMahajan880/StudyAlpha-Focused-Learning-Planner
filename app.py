import streamlit as st
import pandas as pd
from datetime import date

from src.planner import generate_plan
from src.rebalancer import rebalance_plan
from src.evaluator import find_weak_topics
from src.recommender import recommend_next

st.set_page_config(page_title="Study Alpha", layout="wide")

def ensure_schema(df):
    required = {
        "Allocated Hours": 0.0,
        "Hours Spent": 0.0,
        "Remaining Hours": 0.0,
        "Status": "Pending"
    }
    for col, default in required.items():
        if col not in df.columns:
            df[col] = default
    return df

st.title("📘 Study Alpha – Focused Learning Planner")
st.caption(
    "Study assistance for exam-focused preparation and daily consistency-based learning · Built by Shubham Mahajan"
)

st.divider()

exam_date = st.date_input("Exam Date", min_value=date.today())
daily_hours = st.slider("Daily Study Hours", 1, 10, 4)
days_left = max((exam_date - date.today()).days, 1)

st.subheader("📚 Subjects & Topics")

subjects = []
subject_count = st.number_input("Number of Subjects", 1, 6, 1)

for i in range(subject_count):
    with st.expander(f"Subject {i+1}"):
        name = st.text_input("Subject Name", key=f"name_{i}")
        topics = st.text_area("Topics (comma separated)", key=f"topics_{i}")
        if name and topics:
            subjects.append({
                "name": name,
                "topics": [t.strip() for t in topics.split(",")]
            })

if st.button("🚀 Generate Study Plan"):
    plan = generate_plan(subjects, exam_date, daily_hours)
    df = ensure_schema(pd.DataFrame(plan))
    st.session_state["plan"] = df
    st.success("Study plan generated successfully.")

if "plan" in st.session_state:
    df = ensure_schema(st.session_state["plan"])

    st.divider()
    st.subheader("📊 Study Progress")

    total = df["Allocated Hours"].sum()
    spent = df["Hours Spent"].sum()
    remaining = df["Remaining Hours"].sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Planned Hours", round(total, 1))
    c2.metric("Hours Studied", round(spent, 1))
    c3.metric("Remaining Hours", round(remaining, 1))

    progress = int((spent / total) * 100) if total else 0
    st.progress(progress)

    if days_left <= 5 and remaining > 0:
        st.toast("⏰ Exam is near. Increase focus on remaining topics.", icon="⚠️")

    st.divider()
    st.subheader("🎯 Today’s Study Focus")

    today_tasks = df[df["Remaining Hours"] > 0].sort_values("Remaining Hours").head(3)
    for _, row in today_tasks.iterrows():
        st.info(
            f"{row['Subject']} → {row['Topic']} | Remaining: {round(row['Remaining Hours'],1)} hrs"
        )

    st.divider()
    st.subheader("🗓️ Study Plan (Log Your Study Time)")

    edited_df = st.data_editor(df, num_rows="dynamic")
    edited_df = ensure_schema(edited_df)

    updated_df = rebalance_plan(edited_df, exam_date, daily_hours)
    st.session_state["plan"] = updated_df

    weak_topics = find_weak_topics(updated_df.to_dict("records"))

    st.divider()
    st.subheader("🧠 Recommendation")
    st.info(recommend_next(weak_topics, days_left))
