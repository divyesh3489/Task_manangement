"""
API router for version 1 of the Task Management API.
"""
from fastapi import APIRouter

router = APIRouter()

from api.v1.routes import tasks

router.include_router(tasks.router)
