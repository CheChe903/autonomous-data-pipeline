from __future__ import annotations

from fastapi import APIRouter, UploadFile, File, Form

from app.schemas.upload import UploadResponse
from app.services.upload_service import UploadService

router = APIRouter(prefix="/upload", tags=["upload"])

service = UploadService()


@router.post("", response_model=UploadResponse)
async def upload(
    file: UploadFile = File(..., description="이미지/동영상 파일"),
    metadata: str = Form(..., description="JSON 문자열 메타데이터"),
):
    # 컨트롤러는 요청 파싱만 담당, 로직은 서비스로 위임
    return service.process_upload(file, metadata)
