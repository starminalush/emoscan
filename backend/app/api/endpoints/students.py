from fastapi import APIRouter, Depends, Query

from crud.student import get_all_students
from api.deps import get_db, get_c3_client
from schemas.students import Student
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

router = APIRouter()


@router.get("/", response_model=list[Student | None])
async def get_students(
    db: AsyncSession = Depends(get_db),
    s3_client=Depends(get_c3_client),
    page: int = Query(1, gt=0),
    limit: int = Query(5, gt=0),
):
    start_index = (page - 1) * limit
    all_students = await get_all_students(db=db, start_index=start_index, limit=limit)
    logger.info(all_students)
    result = []
    if all_students:
        for t in all_students:
            # формируем ссылку на s3
            image_path = f"{t['datetime'].strftime('%Y-%m-%d')}/{str(t['task_id'])}/{t['image_uuid']}.jpg"
            url = await s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": "logs", "Key": image_path},
                ExpiresIn=400,
            )
            result.append(Student(track_id=t["track_id"], image_url=url))
    return result
