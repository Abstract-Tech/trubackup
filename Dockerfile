FROM mongo:3.2.16 as mongo

FROM python:3.6-alpine

RUN apk add mariadb-client

RUN pip install -U pip
COPY egg /egg

RUN pip install -U pip && \
    pip install /egg
# Uncomment to debug
# RUN pip install pdbpp

CMD /usr/local/bin/edxbackup

# Experimental strategy: we copy the binary files (executable and libraries) that we need
# from a specific version of the docker image.
# This allows us to tie mongodb version to a specific docker image, and not
# be limited to the version shipped with Alpine Linux
# The fact that we're copying libc suggests we might consider switching to a
# libc-based distro instead of a musl-based one
RUN mkdir /lib64
COPY --from=mongo /usr/bin/mongorestore /usr/bin/mongodump /usr/bin/
COPY --from=mongo /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=mongo /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libpthread.so.0 /usr/lib/x86_64-linux-gnu/libcrypto.so.1.0.0 /usr/lib/x86_64-linux-gnu/libssl.so.1.0.0 /usr/lib/x86_64-linux-gnu/
