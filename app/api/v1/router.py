from fastapi import APIRouter

from app.api.v1.routes import auth, workflows

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])

