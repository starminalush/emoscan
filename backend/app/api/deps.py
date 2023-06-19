from os import getenv
from typing import Generator

import aioboto3
from core.db.database import SessionLocal


async def get_db() -> Generator:
    async with SessionLocal() as session:
        yield session


async def get_c3_client():
    s3_session = aioboto3.Session()
    async with s3_session.client(service_name='s3',
                                 endpoint_url=getenv('S3_ENDPOINT_URL'),
                                 aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
                                 aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY_ID")) as client:
        yield client
