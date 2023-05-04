# edxbackup

edxbackup is a thin wrapper around [restic](https://restic.net/).

edxbackup supports backing up MySQL (using [mydumper](https://github.com/mydumper/mydumper)), MongoDB (using mongodb-tools) and S3 buckets (using minio-client python module).

edxbackup is configured using JSON file and environment variables

edxbackup is a CLI tool that supports following operations:

1. backup: performs backup from sources listed in JSON config. edxbackup always overwrites `hostname` of backup to track backup groups (backups done by individual `edxbackup backup` invovations);
2. list: prints a list of available backup groups followed by backup date;
2. show: prints contents of specific backup group
3. restore: performs restore from given backup group.
