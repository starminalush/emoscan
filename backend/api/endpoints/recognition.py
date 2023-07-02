from uuid import UUID

from api.deps import get_c3_client, get_db
from fastapi import APIRouter, Body, Depends, File, UploadFile
from schemas.emotion_recognition import EmotionRecognitionResponse
from services.frame_processing import recognize, write_logs
from sqlalchemy.ext.asyncio import AsyncSession
from converters import cnvt_image_to_base64

router = APIRouter()


@router.post("/", response_model=list[EmotionRecognitionResponse])
async def recognize_emotions_on_image(
    task_id: UUID = Body(...),
    upload_file: UploadFile = File(
        ..., content_type=["image/jpeg", "image/png", "image/jpg"]
    ),
    db: AsyncSession = Depends(get_db),
    s3_client=Depends(get_c3_client),
):
    """Recognize emotions on faces in image file.

    Args:
        task_id: ID of recognition task. Ex: lesson ID.
        upload_file: Image or frame from video.
        db: SQLAlchemy local session.
        s3_client: Class instance of S3Client.

    Returns:
        List of EmotionRecognitionResponse.
    """
    img_bytes = await upload_file.read()
    emotion_recognition_results: list[
        EmotionRecognitionResponse | None
    ] = await recognize(img_bytes=cnvt_image_to_base64(img_bytes))
    if emotion_recognition_results:
        await write_logs(
            task_id=task_id,
            emotion_recognition_results=emotion_recognition_results,
            db=db,
            s3_client=s3_client,
            img_bytes=(await upload_file.read()),
        )
        return emotion_recognition_results
    return []
