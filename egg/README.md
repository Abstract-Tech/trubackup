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

Dump example:

    docker run --network host -v /path/to_dump/destination:/tmp/mongodump --rm -ti \
    silviot/edx-backup edxbackup edx_dump \
    --edx-config /edx/app/edxapp/lms.auth.json \
    --dump-location /tmp/mongodump

Restore example:

    docker run --network host -v /path/to_dump/edxdump-2019-02-26T14:46:04.323836:/tmp/mongodump --rm -ti \
    silviot/edx-backup edxbackup edx_restore \
    --edx-config /edx/app/edxapp/lms.auth.json \
    --dump-location /tmp/mongodump


DISCLAIMER
----------

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

