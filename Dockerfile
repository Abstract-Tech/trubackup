FROM alpine:3.10 as mydumper

ENV PACKAGES="mariadb-client" \
    LIB_PACKAGES="glib-dev mariadb-dev zlib-dev pcre-dev libressl-dev" \
    BUILD_PACKAGES="cmake build-base git"

RUN apk --no-cache add \
          $PACKAGES \
          $BUILD_PACKAGES \
          $LIB_PACKAGES
RUN git clone --single-branch --branch v0.9.5 https://github.com/maxbube/mydumper.git /opt/mydumper-src/
RUN cd /opt/mydumper-src/ && \
    cmake . && \
    make

# Mention the mongo image so that we can copy its binaries
FROM mongo:3.2.16 as mongo

# Compile our egg dependencies (swift/keystone)
FROM python:3.7-alpine3.10 as dev
RUN apk add alpine-sdk linux-headers
COPY egg /egg

RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -e /egg && \
    pip --no-cache-dir wheel --wheel-dir=/wheelhouse /egg && \
    rm /wheelhouse/*-none-*

FROM python:3.7-alpine3.10
COPY --from=dev /wheelhouse /wheelhouse
COPY egg /egg

RUN apk --no-cache add glib zlib pcre libressl mariadb-connector-c

RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -e /egg --find-links /wheelhouse
# Uncomment to debug
# RUN pip install --no-cache-dir pdbpp

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
COPY --from=mydumper /opt/mydumper-src/mydumper /opt/mydumper-src/myloader /usr/bin/

CMD ["/usr/sbin/crond", "-f", "-L", "8"]
