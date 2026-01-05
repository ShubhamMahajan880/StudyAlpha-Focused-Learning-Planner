def find_weak_topics(progress):
    return [
        item["Topic"]
        for item in progress
        if item["Remaining Hours"] > 0
    ]
