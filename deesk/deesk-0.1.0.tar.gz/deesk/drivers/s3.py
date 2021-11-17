from __future__ import annotations

import aioboto3
import mimetypes
import typing as t
from botocore.exceptions import ClientError

from deesk.drivers.base import Driver
from deesk.protocols import FileReader


class S3Driver(Driver):
    def __init__(
        self,
        bucket: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str = None,
        profile_name: str = None,
        endpoint_url: str = None,
    ) -> None:
        self.bucket = bucket
        self.endpoint_url = endpoint_url
        self.session = aioboto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
            profile_name=profile_name,
        )

    async def write(self, path: str, data: t.IO[bytes]) -> None:
        mime_type = mimetypes.guess_type(path)
        async with self.session.client('s3', endpoint_url=self.endpoint_url) as client:
            await client.upload_fileobj(
                data,
                self.bucket,
                path,
                ExtraArgs={
                    'ContentType': mime_type[0],
                },
            )

    async def read(self, path: str) -> FileReader:
        async with self.session.client('s3', endpoint_url=self.endpoint_url) as client:
            try:
                response = await client.get_object(Bucket=self.bucket, Key=path)
            except ClientError as ex:
                if ex.response['Error']['Code'] == 'NoSuchKey':
                    raise FileNotFoundError('File not found: %s' % path)
                raise
            else:
                return response['Body']

    async def delete(self, path: str) -> None:
        async with self.session.client('s3', endpoint_url=self.endpoint_url) as client:
            try:
                await client.delete_object(Bucket=self.bucket, Key=path)
            except ClientError as ex:
                if ex.response['Error']['Code'] == 'NoSuchKey':
                    raise FileNotFoundError()
                raise

    async def exists(self, path: str) -> bool:
        async with self.session.client('s3', endpoint_url=self.endpoint_url) as client:
            try:
                await client.get_object(Bucket=self.bucket, Key=path)
            except ClientError as ex:
                if ex.response['Error']['Code'] == 'NoSuchKey':
                    return False
                raise
            else:
                return True
