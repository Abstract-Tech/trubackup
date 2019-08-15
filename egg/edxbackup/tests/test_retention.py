from datetime import datetime
from datetime import timedelta


def test_to_delete():
    from edxbackup.retention import to_delete
    from edxbackup.retention import retention_from_conf

    TEST_RETENTION_POLICY = retention_from_conf(
        (({"days": 1}, 7), ({"days": 7}, 4), ({"days": 28}, 12))
    )

    TEST_DATA = [
        {
            "now": datetime(2017, 2, 2, 0, 0),
            "elements": [
                (datetime(2017, 2, 1, 12, 0), "keep"),
                (datetime(2017, 1, 31, 12, 0), "keep"),
                (datetime(2017, 1, 30, 12, 0), "keep"),
                (datetime(2017, 1, 25, 12, 0), "keep"),
                (datetime(2017, 1, 20, 12, 0), "keep"),
                (datetime(2017, 1, 18, 12, 0), "toss"),  # we have the one from the 20th
            ],
        },
        {
            "now": datetime(2017, 2, 2, 0, 0),
            "elements": [
                (datetime(2017, 2, 1, 12, 0), "keep"),
                (datetime(2017, 1, 31, 12, 0), "keep"),
                (datetime(2017, 1, 31, 10, 0), "toss"),
                (datetime(2017, 1, 31, 9, 0), "toss"),
                (datetime(2017, 1, 31, 8, 0), "toss"),
                (datetime(2017, 1, 30, 12, 0), "keep"),
                (datetime(2017, 1, 20, 12, 0), "keep"),
                (datetime(2017, 1, 17, 12, 0), "toss"),
                (datetime(2017, 1, 16, 12, 0), "toss"),
            ],
        },
        {
            "now": datetime(2017, 2, 2, 0, 0),
            "elements": [
                (datetime(2017, 2, 1, 12, 0), "keep"),
                (datetime(2017, 1, 31, 12, 0), "keep"),
                (datetime(2017, 1, 30, 12, 0), "keep"),
                (datetime(2017, 1, 20, 12, 0), "keep"),
            ],
        },
    ]

    for args in TEST_DATA:
        result = to_delete(TEST_RETENTION_POLICY, args["elements"], args["now"])
        assert result == [el for el in args["elements"] if el[1] == "toss"]


def test_to_delete_one_year():
    from edxbackup.retention import table_info
    from edxbackup.retention import to_delete

    TEST_RETENTION_POLICY = {
        timedelta(days=1): 8,
        timedelta(days=7): 5,
        timedelta(days=28): 3,
    }

    # We start simulating 200 snapshots 12 hours apart from one another
    # spanning 100 days
    now = datetime(2017, 2, 2, 14, 0)
    elements = []

    # The `elements` in this test happen to be integers ascending in time
    i = 0
    INITIALCOUNT = 300
    while i < INITIALCOUNT:
        elements.insert(
            0, (now - ((INITIALCOUNT - i) * timedelta(hours=12)), "{}".format(i))
        )
        i += 1

    for _ in range(365):  # simulate a year of daily snapshots and deletions
        now += timedelta(days=1)
        elements.insert(0, (now, i))
        i += 1

        # print("\n" + table_info(elements, now, TEST_RETENTION_POLICY))

        # remove the elements that `to_delete` reports as unnecessary
        elements_to_delete = {
            el[1] for el in to_delete(TEST_RETENTION_POLICY, elements, now=now)
        }
        elements = [el for el in elements if el[1] not in elements_to_delete]

        # We should have one snapshot per defined period plus one for the oldest
        # period (the one starting at EPOCH)
        assert len(elements) == sum(TEST_RETENTION_POLICY.values()) + 1


def test_validate_retention_policy():
    from edxbackup.retention import validate_retention_policy

    assert (
        validate_retention_policy(
            {timedelta(days=1): 7, timedelta(days=7): 2, timedelta(days=30): 3}
        )
        is False
    )

    assert (
        validate_retention_policy(
            {timedelta(days=1): 7, timedelta(days=7): 5, timedelta(days=30): 3}
        )
        is False
    )

    assert (
        validate_retention_policy(
            {timedelta(days=1): 7, timedelta(days=7): 4, timedelta(days=28): 3}
        )
        is True
    )

    assert (
        validate_retention_policy(
            {timedelta(days=1): 8, timedelta(days=7): 5, timedelta(days=28): 3}
        )
        is True
    )
