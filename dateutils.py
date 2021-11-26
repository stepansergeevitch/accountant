from datetime import datetime, timedelta, date
from typing import List, Tuple


def datetime_range_steps(
    from_date: date, to_date: date, step_days: int
) -> List[Tuple[datetime]]:
    def date_to_datetime(d: date) -> datetime:
        return datetime(year=d.year, month=d.month, day=d.day)

    from_date = date_to_datetime(from_date)
    to_date = date_to_datetime(to_date)

    def inc_step(dt: datetime, step_days: int) -> datetime:
        return dt + timedelta(days=step_days + 1) - timedelta(seconds=1)

    left = from_date
    right = min(inc_step(left, step_days), to_date)
    while left < to_date:
        yield (left, right)
        left = right + timedelta(seconds=1)
        right = min(inc_step(left, step_days), to_date)


def get_quarters_for_year(year: int) -> List[Tuple[datetime]]:
    return [
        (datetime(year, 1, 1), datetime(year, 3, 31)),
        (datetime(year, 4, 1), datetime(year, 6, 30)),
        (datetime(year, 7, 1), datetime(year, 9, 30)),
        (datetime(year, 10, 1), datetime(year, 12, 31)),
    ]
