def recommend_next(weak_topics, days_left):
    if not weak_topics:
        return "All topics are completed. Shift focus to revision and mock tests."

    if days_left <= 3:
        return f"Exam is very close. Focus immediately on: {', '.join(weak_topics[:2])}"

    return f"Continue studying. Prioritize these topics next: {', '.join(weak_topics[:3])}"
