FROM alpine:3.17 as mydumper

ENV PACKAGES="mariadb-client" \
    LIB_PACKAGES="glib-dev mariadb-dev zlib-dev pcre-dev openssl-dev" \
    BUILD_PACKAGES="cmake build-base git"

RUN apk --no-cache add \
          $PACKAGES \
          $BUILD_PACKAGES \
          $LIB_PACKAGES
RUN git clone --single-branch --branch v0.9.5 https://github.com/maxbube/mydumper.git /opt/mydumper-src/
RUN cd /opt/mydumper-src/ && \
    cmake . && \
    make

# Compile our egg dependencies (swift/keystone)
FROM python:3.11-alpine3.17 as dev
RUN apk add linux-headers gcc musl-dev
COPY egg /egg

RUN pip install --no-cache-dir -U pip && \
    pip --no-cache-dir wheel --wheel-dir=/wheelhouse /egg && \
    `# Only keep binary wheels` \
    rm /wheelhouse/*-none-*

FROM python:3.11-alpine3.17
COPY --from=dev /wheelhouse /wheelhouse
COPY egg /egg

RUN apk --no-cache add glib zlib pcre openssl mariadb-connector-c mongodb-tools rclone

RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -e /egg --find-links /wheelhouse
# Uncomment to debug
# RUN pip install --no-cache-dir pdbpp

CMD /usr/local/bin/edxbackup

COPY --from=mydumper /opt/mydumper-src/mydumper /opt/mydumper-src/myloader /usr/bin/

CMD ["/usr/sbin/crond", "-f", "-L", "8"]

ENV XDG_CONFIG_HOME=/etc
