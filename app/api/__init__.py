from fastapi import APIRouter

from app.api import upload, images, stats, dataset

api_router = APIRouter()
api_router.include_router(upload.router, tags=["upload"])
api_router.include_router(images.router, tags=["images"])
api_router.include_router(dataset.router, tags=["download"])
api_router.include_router(stats.router, tags=["stats"])
