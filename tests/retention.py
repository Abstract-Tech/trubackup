from datetime import datetime
from datetime import timedelta
from subprocess import Popen


BASE_DATE = datetime.fromisoformat("2012-11-01")

full_year = [BASE_DATE + timedelta(i) for i in range(365)]

for day in full_year:
    edxbackup_args = ["edxbackup", "backup", "--time", day.isoformat()]

    Popen(edxbackup_args).wait()
