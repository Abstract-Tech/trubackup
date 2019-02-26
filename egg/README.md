edX Backup
==========

Introduction
------------

Simple utility scripts to dump and restore an Open edX instance.

A docker image can be built with:

    make build-image

Usage
-----

Parameters can be passed either as environment variables or on the command line.

Mongodb restore example:

    docker run --network tutor_local_default -v $(pwd)/tum-dump/mongodump.tar.gz:/tmp/mongodump.tar.gz --rm -ti silviot/edx-backup edxbackup mongo_restore --mongo-host mongodb --input-file /tmp/mongodump.tar.gz

Mysql restore example:

    docker run --network tutor_local_default -v $(pwd)/tum-dump/mysql_dump.sql.gz:/tmp/mysql_dump.sql.gz --rm -ti silviot/edx-backup edxbackup mysql_restore --mysql-host mysql --mysql-user root --mysql-password FOOBAR --input-file /tmp/mysql_dump.sql.gz


DISCLAIMER
----------

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

