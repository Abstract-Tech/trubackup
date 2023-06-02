edxbackup
=========

edxbackup is a thin wrapper around `restic <https://restic.net/>`__.

edxbackup supports backing up MySQL (using
`mydumper <https://github.com/mydumper/mydumper>`__), MongoDB (using
mongodb-tools) and S3 buckets (using minio-client python module).

edxbackup is configured using JSON file and environment variables

edxbackup is a CLI tool that supports following operations:

1. backup: performs backup from sources listed in JSON config. edxbackup
   always overwrites ``hostname`` of backup to track backup groups
   (backups done by individual ``edxbackup backup`` invovations);
2. list: prints a list of available backup groups followed by backup
   date;
3. show: prints contents of specific backup group
4. restore: performs restore from given backup group.

To run edxbackup regularly, you can use systemd service and timer in
systemd/ directory.
