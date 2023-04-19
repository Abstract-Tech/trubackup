#!/usr/bin/env python3
from subprocess import Popen

import os


def env_policy():
    return {
        "daily": os.environ.get("EDXBACKUP_KEEP_WITHIN_DAILY"),
        "weekly": os.environ.get("EDXBACKUP_KEEP_WITHIN_WEEKLY"),
        "monthly": os.environ.get("EDXBACKUP_KEEP_WITHIN_MONTHLY"),
        "yearly": os.environ.get("EDXBACKUP_KEEP_WITHIN_YEARLY"),
    }


def describe_policy(policy):
    if policy["daily"] is not None:
        print(f"Will keep daily backups within {policy['daily']}")
    if policy["weekly"] is not None:
        print(f"Will keep weekly backups within {policy['weekly']}")
    if policy["monthly"] is not None:
        print(f"Will keep monthly backups within {policy['monthly']}")
    if policy["yearly"] is not None:
        print(f"Will keep yearly backup within {policy['yearly']}")


def enforce_policy(policy):
    enforce_args = ["restic", "forget", "--prune", "--group-by", "tags"]

    if policy["daily"] is not None:
        enforce_args += ["--keep-within-daily", policy["daily"]]
    if policy["weekly"] is not None:
        enforce_args += ["--keep-within-weekly", policy["weekly"]]
    if policy["monthly"] is not None:
        enforce_args += ["--keep-within-monthly", policy["monthly"]]
    if policy["yearly"] is not None:
        enforce_args += ["--keep-within-yearly", policy["yearly"]]

    Popen(enforce_args).wait()


policy = env_policy()
describe_policy(policy)
enforce_policy(policy)
