from dateutil.relativedelta import relativedelta
from datetime import datetime


def partition_by_date(edges, start_inclusive, end_exclusive, duration_in_month):
    start_months = list_of_months(start_inclusive, end_exclusive, duration_in_month)
    edges.sort(
        key=lambda e: e.timestamp
    )
    partitions = []
    left = start_inclusive
    for month in start_months[1:]:
        right = month
        partition = list(
            filter(
                lambda e: is_in_between(e, left, right),
                edges
            )
        )
        partitions.append(partition)
        left = right
    return partitions


def is_in_between(edge, start, next_start):
    return start <= edge.timestamp < next_start


def list_of_months(start, end, duration):
    results = []
    current = datetime(start.year, start.month, start.day)
    while current < end:
        results.append(current)
        current += relativedelta(months=duration)
    results.append(current)
    return results
