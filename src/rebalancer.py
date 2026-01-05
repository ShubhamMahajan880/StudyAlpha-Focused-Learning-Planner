from datetime import date

def rebalance_plan(df, exam_date, daily_hours):
    today = date.today()
    days_left = max((exam_date - today).days, 1)

    # Ensure numeric
    df["Hours Spent"] = df["Hours Spent"].fillna(0).astype(float)
    df["Remaining Hours"] = df["Allocated Hours"] - df["Hours Spent"]

    pending = df[df["Remaining Hours"] > 0]

    if pending.empty:
        df["Status"] = "Completed"
        df["Remaining Hours"] = 0
        return df

    total_remaining_hours = days_left * daily_hours
    new_hours_per_topic = round(total_remaining_hours / len(pending), 2)

    df.loc[df["Remaining Hours"] > 0, "Allocated Hours"] = new_hours_per_topic
    df["Remaining Hours"] = (df["Allocated Hours"] - df["Hours Spent"]).clip(lower=0)

    df.loc[df["Remaining Hours"] == 0, "Status"] = "Completed"
    df.loc[df["Remaining Hours"] > 0, "Status"] = "In Progress"

    return df
