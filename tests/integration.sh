#!/usr/bin/env sh

set -x

./populate.sh

# Perform backup & restore cycle
BACKUP_OUTPUT=$(edxbackup backup)
echo $BACKUP_OUTPUT | grep -q "failed to backup" && echo "Backup failed" && exit 1

BACKUP_ID=$(echo $BACKUP_OUTPUT | tail -n1)
RESTORE_OUTPUT=$(edxbackup restore $BACKUP_ID)
echo $RESTORE_OUTPUT | grep -q "failed to restore" && echo "Restore failed" && exit 1
