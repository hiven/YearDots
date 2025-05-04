"""
Calendar helpers used only by the main blueprint.
"""

from datetime import date, timedelta
from typing import List


def week_span(ref: date | None = None, first_weekday: int = 0) -> List[date]:
    """Seven dates (Mon-Sun by default) for the week that contains *ref*."""
    if ref is None:
        ref = date.today()

    start = ref - timedelta(days=(ref.weekday() - first_weekday) % 7)
    return [start + timedelta(days=i) for i in range(7)]


def rolling_weeks(
    weeks: int,
    ref: date | None = None,
    first_weekday: int = 0,
    transpose: bool = True,
) -> List[List[date]]:
    """
    Grid covering *weeks* weeks ending with the week that contains *ref*.

    Returns 7 rows × *weeks* columns (row-0 = Monday) when *transpose* is True.
    Suitable for vertical heat-map layouts.
    """
    if ref is None:
        ref = date.today()

    cols = [
        week_span(ref - timedelta(days=7 * w), first_weekday)
        for w in range(weeks)
    ][::-1]                      # earliest week on the left

    return [list(r) for r in zip(*cols)] if transpose else cols
