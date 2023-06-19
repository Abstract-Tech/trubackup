export MYSQL_USER=root
export MYSQL_PASSWORD=foobar

export POSTGRES_USER=root
export POSTGRES_PASSWORD=foobar

export MONGO_USER=root
export MONGO_PASSWORD=foobar

export MINIO_ACCESS_KEY=access_key
export MINIO_SECRET_KEY=secret_key

export MC_HOST_test=http://$MINIO_ACCESS_KEY:$MINIO_SECRET_KEY@localhost:19000

export RESTIC_REPOSITORY="rest:http://localhost:18000"
export RESTIC_PASSWORD="foobar"

export EDXBACKUP_CONFIG_PATH=./edxbackup.json
