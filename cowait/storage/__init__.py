# flake8: noqa: F401

from .backends import StorageBackends

from fsspec.implementations.local import LocalFileOpener
from fsspec.implementations.http import HTTPFile
from fsspec.implementations.ftp import FTPFile

FileFormats = [LocalFileOpener, HTTPFile, FTPFile]

# HDFS (requires pyarrow)
try:
    from fsspec.implementations.hdfs import HDFSFile
    FileFormats.append(HDFSFile)
except ImportError:
    pass

# S3 (requires s3fs)
try:
    from s3fs import S3File
    FileFormats.append(S3File)
except ImportError:
    pass
