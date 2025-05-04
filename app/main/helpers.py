from datetime import date, timedelta


def week_span() -> list[str]:
    today   = date.today()
    monday  = today - timedelta(days=today.weekday())
    return [
        (monday + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)
    ]


def overall_grid() -> list[list[str]]:
    today   = date.today()
    monday  = today - timedelta(days=today.weekday())   # start of this week

    cols = []
    for w in range(22):
        week_start = monday - timedelta(days=7 * (21 - w))   # 21 … 0
        cols.append([
            (week_start + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(7)
        ])

    return [list(row) for row in zip(*cols)]
