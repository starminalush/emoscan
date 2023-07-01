import asyncio
import io
from os import getenv

import aioboto3


class S3Client:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._session = None
        self._client = None
        self._bucket_name = getenv("BUCKET")

    async def close(self):
        if self._client is not None:
            await self._client.close()

        if self._session is not None:
            await self._session.close()

    @classmethod
    async def create(cls):
        self = cls()
        if not self._client:
            if not self._session:
                self._session = aioboto3.Session()
            self._client = self._session.client(
                service_name="s3",
                endpoint_url=getenv("S3_ENDPOINT_URL"),
                aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
            )
        return self

    async def upload_file(self, filename: str, img_bytes: bytes):
        try:
            async with self._client as client:
                await client.upload_fileobj(
                    io.BytesIO(img_bytes), self._bucket_name, filename
                )
        except Exception as e:
            raise e
