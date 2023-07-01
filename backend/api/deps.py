from os import getenv
from typing import Generator
from core.s3.s3client import S3Client
import aioboto3

from core.db.database import SessionLocal


async def get_db() -> Generator:
    async with SessionLocal() as session:
        yield session


async def get_c3_client():
    return await S3Client.create()
