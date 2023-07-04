from typing import Generator

from core.db.database import SessionLocal
from core.s3.s3client import S3Client


async def get_db() -> Generator:
    async with SessionLocal() as session:
        yield session


async def get_c3_client():
    async with S3Client() as s3_client:
        yield s3_client
