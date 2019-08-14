"""Tools useful to decide which backups to keep to adhere to a retention policy
"""
from datetime import datetime
from datetime import timedelta
from terminaltables import SingleTable


def validate_retention_policy(retention_policy):
    """Check that a given retention policy is viable in the long run.
    For a retention policy to work, it's essential that the cardinality of
    each retained period size is enough to make sure there will be a candidate
    when the longer period kicks in.
    One more condition needed is that each retention period is a multiple of the
    previous one, so that they align at the same boundary.

    :param retention_policy: dictionary representing the retention_policy.
        keys should be timdeltas, values integers.

    :returns: True if the retention policy is valid, False otherwise.
    """
    previous_time_covered = timedelta.max
    previous_duration = timedelta(seconds=1)
    for duration, howmany in sorted(retention_policy.items()):
        current_time_covered = duration * howmany
        if previous_time_covered != timedelta.max:
            if duration.total_seconds() % previous_duration.total_seconds() != 0:
                return False
        if previous_time_covered < duration:
            return False
        previous_time_covered = current_time_covered
        previous_duration = duration
    return True


def colourize(li, colour):
    return ["\x1b[3{}m{}\x1b[0m".format(colour, cell) for cell in li]


def table_info(elements, now, retention_policy):
    """Print a table showing the elements that should be deleted alongside the periods
    they pertain to.
    """
    elements = sorted(elements, key=lambda x: x[0], reverse=True)

    elements_to_delete = {
        el[1] for el in to_delete(retention_policy, elements, now=now)
    }
    snapshot_rows = []
    for el in elements:
        slot = slot_for(el[0], retention_policy, now)
        if slot[0] == datetime.min:
            slot_duration = "inf"
        else:
            slot_duration = str(slot[1] - slot[0]).split(",")[0]
        el_id = str(el[1]) + (" *" if el[1] in elements_to_delete else "")
        snapshot_rows.append([el[0], el_id, slot[0], slot[1], slot_duration])

    records = []
    current_colour = 1
    for slot in boundaries_for(retention_policy, now):
        while snapshot_rows and snapshot_rows[0][2] > slot[0]:
            records.append(colourize(snapshot_rows.pop(0), current_colour))
        if snapshot_rows and snapshot_rows[0][2] < slot[0]:
            slot_info = ["---", "---", slot[0], slot[1], slot[1] - slot[0]]
            records.append(colourize(slot_info, current_colour))
        current_colour = (current_colour + 1) % 8 + 1

    # One more pass to include very old snapshots
    previous_slot = slot
    while snapshot_rows:
        row = snapshot_rows.pop(0)
        records.append(colourize(row, current_colour))
        if (row[2], row[3]) != previous_slot:
            current_colour = (current_colour + 1) % 8 + 1
        previous_slot = row[2], row[3]

    table_data = [
        ("Timestamp", "Serial #", "Slot begin", "Slot end", "Slot duration")
    ] + records
    table_title = "{date} ({n})".format(date=now.date(), n=len(elements))
    return "\n" + SingleTable(table_data, title=table_title).table


def round_dt(dt, round_to=86400):
    """Round a datetime object to any time lapse in seconds.
    Anchor to a Monday so that if round_to represents a week,
    dt will be rounded to the previous Monday.

    :param dt: datetime.datetime object, default now.
    :type dt: :class:`datetime.datetime`
    :param round_to: closest number of seconds to round to, default 1 day.
    :type round_to: int or timedelta

    >>> now = datetime.now()
    >>> assert round_dt(now) == datetime.combine(now, datetime.min.time())
    >>> assert round_dt(now, round_to=timedelta(1)) == datetime.combine(now, datetime.min.time())
    >>> assert round_dt(datetime(2017, 3, 10, 2, 22), round_to=timedelta(7)) == round_dt(datetime(2017, 3, 6, 0, 0))
    """
    # Set the epoch on a Monday
    EPOCH = datetime.utcfromtimestamp(86400 * 4)
    if isinstance(round_to, timedelta):
        round_to = round_to.total_seconds()
    seconds = (dt - EPOCH).total_seconds()
    return EPOCH + timedelta(seconds=divmod(seconds, round_to)[0] * round_to)


def boundaries_for(retention_policy, now):
    if not validate_retention_policy(retention_policy):
        raise ValueError("Invalid retention policy")
    offset = timedelta(0)
    for period, howmany in sorted(retention_policy.items()):
        for i in range(howmany):
            boundary = round_dt(now - offset - (period * i), period)
            yield (boundary, boundary + period)
        offset += period * howmany
    yield (datetime.min, boundary)


def slot_for(tstamp, retention_policy, now):
    """Given a timestamp, return the timestamp corresponding to the slot
    of the retention_policy for the passed tstamp.

    >>> slot_for(datetime(2017, 1, 25, 14, 0), {timedelta(1): 8, timedelta(7): 5, timedelta(28): 3}, datetime(2017, 2, 3, 14, 0))
    (datetime.datetime(2017, 1, 23, 0, 0), datetime.datetime(2017, 1, 30, 0, 0))
    """
    # Special case for timestamps in the future: we assign the most recent slot anyway
    if tstamp >= now:
        return tuple(boundaries_for(retention_policy, now))[0]
    # as we progress through the retention policy periods,
    # accumulate the total of already evaluated periods in this variable.
    for lower, upper in boundaries_for(retention_policy, now):
        if lower < tstamp <= upper:
            return lower, upper
    return lower, now


def to_delete(retention_policy, elements, now=None):
    """
    Determine what should be removed from `elements` so that `retention_policy` is honoured.

    :param retention_policy: dictionary representing the retention_policy.
        keys should be timdeltas, values integers.
    :type retention_policy: dict
    :param elements: list of 2-tuples (datetime, element)
    :param now: If specified, act as if now is the given date
    :type now: :class:`datetime.date`

    :returns: A pruned `elements` list containing the elements that should be removed.

    Note: timestamps are expected to be in the `tz.tzlocal()` timezone.
    See test data at the bottom of this file as an example.
    """
    if not validate_retention_policy(retention_policy):
        raise ValueError("Invalid retention policy")

    now = now or datetime.utcnow()
    elements = sorted(elements, key=lambda x: x[0], reverse=True)

    filled_slots = set()
    elements_to_delete = []
    for tstamp, element in elements:
        key = slot_for(tstamp, retention_policy, now)
        if key in filled_slots:
            elements_to_delete.append((tstamp, element))
        else:
            filled_slots.add(key)
    return elements_to_delete
