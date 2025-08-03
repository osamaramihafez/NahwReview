from fastapi import APIRouter, Depends, HTTPException
import aiosqlite
from typing import List
import data.schemas as schemas
from data.database import get_db
import services.level_service as level_service
import services.lesson_service as lesson_service

router = APIRouter(prefix="/levels", tags=["levels"])

@router.get("", response_model=List[schemas.Level])
async def get_levels(db: aiosqlite.Connection = Depends(get_db)):
    levels_data = await level_service.get_all_levels(db)
    return [schemas.Level(**level) for level in levels_data]

@router.get("/{level_id}", response_model=schemas.Level)
async def get_level(level_id: int, db: aiosqlite.Connection = Depends(get_db)):
    level_data = await level_service.get_level_by_id(db, level_id)
    if not level_data:
        raise HTTPException(status_code=404, detail="Level not found")
    return schemas.Level(**level_data)

@router.post("", response_model=schemas.Level)
async def create_level(level: schemas.LevelCreate, db: aiosqlite.Connection = Depends(get_db)):
    level_data = await level_service.create_level(db, level)
    return schemas.Level(**level_data)

@router.put("/{level_id}", response_model=schemas.Level)
async def update_level(level_id: int, level: schemas.LevelCreate, db: aiosqlite.Connection = Depends(get_db)):
    level_data = await level_service.update_level(db, level_id, level)
    if not level_data:
        raise HTTPException(status_code=404, detail="Level not found")
    return schemas.Level(**level_data)

@router.delete("/{level_id}")
async def delete_level(level_id: int, db: aiosqlite.Connection = Depends(get_db)):
    success = await level_service.delete_level(db, level_id)
    if not success:
        raise HTTPException(status_code=404, detail="Level not found")
    return {"message": "Level deleted successfully"}

@router.get("/{level_id}/lessons", response_model=List[schemas.Lesson])
async def get_lessons_by_level(level_id: int, db: aiosqlite.Connection = Depends(get_db)):
    lessons_data = await lesson_service.get_lessons_by_level(db, level_id)
    return [schemas.Lesson(**lesson) for lesson in lessons_data]

@router.get("/{level_id}/next", response_model=schemas.Level)
async def get_next_level(level_id: int, db: aiosqlite.Connection = Depends(get_db)):
    """Get the next level"""
    next_level_data = await level_service.get_next_level(db, level_id)
    if not next_level_data:
        raise HTTPException(status_code=404, detail="No next level found")
    return schemas.Level(**next_level_data)
