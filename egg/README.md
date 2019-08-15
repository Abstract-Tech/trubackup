edX Backup
==========

Introduction
------------

Dump mysql and mongodb databases. Uses mydumper for mysql and mongodump for mongodb.

Usage
-----

Prepare a file with info about yout mysql and mongo databases.
For mysql a user with FLUSH privileges is needed:

```json
{
    "mysql": [{
        "dbname": "test",
        "host": "127.0.0.1",
        "user": "root",
        "password": "foobar",
        "port": "3309"
    }],
    "mongo": {
        "dbname": "edxapp",
        "host": "localhost",
        "user": "edxapp",
        "password": "secret",
        "port": "27017"
    }
}
```

Save the file and point edxdump to it:

    docker run \
        --network host \
        -v /path/to/dump/destination:/destination \
        -v /path/to/config/file.json:/etc/edxbackup.json \
        --rm \
        silviot/edx-backup edxbackup edx_dump

Restore example:

    docker run
        --network host \
        -v /path/to/dump/destination:/destination \
        -v /path/to/config/file.json:/etc/edxbackup.json \
        --rm \
            silviot/edx-backup edxbackup edx_restore


Building
--------

A docker image can be built with:

    make build-image


DISCLAIMER
----------

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
