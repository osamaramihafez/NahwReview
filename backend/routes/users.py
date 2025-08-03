from fastapi import APIRouter, Depends, HTTPException
import aiosqlite
from typing import List
import data.schemas as schemas
from data.database import get_db
import services.user_service as user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}/progress", response_model=List[schemas.UserProgress])
async def get_user_progress(user_id: str, db: aiosqlite.Connection = Depends(get_db)):
    progress_data = await user_service.get_user_progress(db, user_id)
    return [schemas.UserProgress(**progress) for progress in progress_data]

@router.post("/{user_id}/progress", response_model=schemas.UserProgress)
async def update_progress(user_id: str, progress: schemas.UserProgressCreate, db: aiosqlite.Connection = Depends(get_db)):
    progress_data = await user_service.update_user_progress(db, user_id, progress.lesson_id, progress.completed, progress.score)
    return schemas.UserProgress(**progress_data)
