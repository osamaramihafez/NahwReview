from fastapi import APIRouter, Depends, HTTPException
import aiosqlite
from typing import List
import schemas
from database import get_db
import services.lesson_service as lesson_service
import services.exercise_service as exercise_service

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.get("/{lesson_id}", response_model=schemas.Lesson)
async def get_lesson(lesson_id: int, db: aiosqlite.Connection = Depends(get_db)):
    lesson_data = await lesson_service.get_lesson_by_id(db, lesson_id)
    if not lesson_data:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return schemas.Lesson(**lesson_data)

@router.post("", response_model=schemas.Lesson)
async def create_lesson(lesson: schemas.LessonCreate, db: aiosqlite.Connection = Depends(get_db)):
    lesson_data = await lesson_service.create_lesson(db, lesson)
    return schemas.Lesson(**lesson_data)

@router.get("/{lesson_id}/exercises", response_model=List[schemas.Exercise])
async def get_exercises_by_lesson(lesson_id: int, db: aiosqlite.Connection = Depends(get_db)):
    exercises_data = await exercise_service.get_exercises_by_lesson(db, lesson_id)
    return [schemas.Exercise(**exercise) for exercise in exercises_data]

@router.get("/{lesson_id}/next", response_model=schemas.Lesson)
async def get_next_lesson(lesson_id: int, db: aiosqlite.Connection = Depends(get_db)):
    """Get the next lesson in the same level"""
    next_lesson_data = await lesson_service.get_next_lesson(db, lesson_id)
    if not next_lesson_data:
        raise HTTPException(status_code=404, detail="No next lesson found")
    return schemas.Lesson(**next_lesson_data)
