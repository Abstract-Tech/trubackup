edxbackup
+++++++++

edxbackup is database backup program designed to work with
`openedx <https://openedx.org/>`__ data sources, but not specific to it.

edxbackup is a wrapper around `restic <https://restic.net/>`__.

installation
============

manual
------

Make sure that you have following software installed in your environment:

1. Python 3.11
2. `restic <https://restic.net/>`__
3. `myloader <https://www.mongodb.com/docs/database-tools/>`__
4. `mongodb-tools <https://www.mongodb.com/docs/database-tools/>`__

Then, run ``pip install edxbackup==3.1.1``.

docker
------
``docker pull edxbackup:3.1.1``

running
=======

preparations
------------
You need restic repository set up elsewhere for edxbackup to operate. Consult
`restic docs <https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html>`__
to do it.

Before running edxbackup make sure that ``RESTIC_REPOSITORY`` and
``RESTIC_PASSWORD`` are set.

config
------
You can use ``example/edxbackup.json`` in repo as a reference. All the sections
are mandatory, but you can set ``mysql``, ``mongo`` and ``s3`` to empty list if
you don't want to backup those.

There's two ways to pass config location to edxbackup:

1. Put it in the ``EDXBACKUP_CONFIG_PATH`` environment variable
2. Pass it as the value of ``-c`` or ``--config`` command line flag

If neither is used, edxbackup will /etc/edxbackup.json as fallback.

backup
------
Run ``edxbackup backup``. The last line in it's output will be backup ID.

list & show
-----------
``edxbackup list`` and ``edxbackup show`` are informational commands. You can
use the first one to show a list of available backups and the second one to
inspect individual backup contents.

restore
-------
Run ``edxbackup restore <BACKUP_ID>``. Make sure to replace ``<BACKUP_ID>``
with your backup ID.

running regularily
==================
There's example systemd service & timer in systemd/ directory.

deleting old backups
====================
There's ``contrib/delete_old.py`` script in this repo that will run
`restic forget <https://restic.readthedocs.io/en/latest/060_forget.html>`__
command with arguments adjustable by environment variables. **Make sure that
you read the script before running it. It is destructive.**
