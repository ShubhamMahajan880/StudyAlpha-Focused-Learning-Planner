from datetime import date

def generate_plan(subjects, exam_date, daily_hours):
    today = date.today()
    days_left = max((exam_date - today).days, 1)

    plan = []
    total_topics = sum(len(s["topics"]) for s in subjects)
    hours_per_topic = round((days_left * daily_hours) / total_topics, 2)

    day = 1
    for subject in subjects:
        for topic in subject["topics"]:
            plan.append({
                "Day": day,
                "Subject": subject["name"],
                "Topic": topic,
                "Allocated Hours": hours_per_topic,
                "Hours Spent": 0.0,
                "Remaining Hours": hours_per_topic,
                "Status": "Pending"
            })
            if day < days_left:
                day += 1

    return plan
