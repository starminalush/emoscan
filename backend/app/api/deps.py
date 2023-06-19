from typing import Generator

from core.db.database import SessionLocal
from core.minio.s3_client import client as s3_client


async def get_db() -> Generator:
    async with SessionLocal() as session:
        yield session

async def get_c3_client():
    return s3_client