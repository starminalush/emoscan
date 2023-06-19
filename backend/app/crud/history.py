from core.db.models import History
from sqlalchemy.ext.asyncio import AsyncSession


async def write_logs(db: AsyncSession, history_obj: dict):
    history = History(**history_obj)
    db.add(history)
    await db.commit()
    await db.refresh(history)
