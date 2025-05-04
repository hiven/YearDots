from datetime import date, timedelta
from typing import List

def week_span() -> list[str]:
    today  = date.today()
    monday = today - timedelta(days=today.weekday())
    return [
        (monday + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)
    ]


def overall_grid() -> list[list[str]]:
    today  = date.today()
    monday = today - timedelta(days=today.weekday())

    cols = []
    for w in range(22):
        week_start = monday - timedelta(days=7 * (21 - w))
        cols.append([
            (week_start + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(7)
        ])

    return [list(row) for row in zip(*cols)]


def completed_by_habit(records) -> dict[int, set[str]]:
    bucket: dict[int, set[str]] = {}
    for rec in records:
        if rec.completed:
            bucket.setdefault(rec.habit_id, set()).add(
                rec.date.strftime("%Y-%m-%d")
            )
    return bucket
