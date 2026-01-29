from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    # 단순 헬스 체크
    return {"status": "ok"}
