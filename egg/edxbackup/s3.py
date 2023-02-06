import os
import tarfile
import tempfile

import click

from minio import Minio


def dump_s3(host, access_key, secret_key, dump_to, https=True):
    """
    Dump every file at specified S3 host into a .tar.gz archive
    """
    s3_client = Minio(host, access_key, secret_key, secure=https)
    archive = tarfile.open(dump_to, mode="w:gz")

    for bucket in s3_client.list_buckets():
        for obj in s3_client.list_objects(bucket.name, recursive=True):
            _, buf_file = tempfile.mkstemp()

            s3_client.fget_object(bucket.name, obj.object_name, buf_file)

            arcname = os.path.join(bucket.name, obj.object_name)
            archive.add(buf_file, arcname=arcname)

            os.remove(buf_file)

    archive.close()


def restore_s3(host, access_key, secret_key, restore_from, https=True):
    """
    Upload every file from .tar.gz archvie into S3 host
    """
    s3_client = Minio(host, access_key, secret_key, secure=https)
    archive = tarfile.open(restore_from, mode="r:gz")

    for tarinfo in archive:
        if tarinfo.isfile():
            path_parts = tarinfo.name.split(os.path.sep)
            bucket = path_parts[0]
            object_name = os.path.sep.join(path_parts[1:])

            ex_reader = archive.extractfile(tarinfo)
            s3_client.put_object(bucket, object_name, ex_reader, tarinfo.size)
