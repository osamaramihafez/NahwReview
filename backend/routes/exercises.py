from fastapi import APIRouter, Depends, HTTPException
import aiosqlite
from typing import List
import data.schemas as schemas
from data.database import get_db
import services.exercise_service as exercise_service

router = APIRouter(prefix="/exercises", tags=["exercises"])

@router.get("/{exercise_id}", response_model=schemas.Exercise)
async def get_exercise(exercise_id: int, db: aiosqlite.Connection = Depends(get_db)):
    exercise_data = await exercise_service.get_exercise_by_id(db, exercise_id)
    if not exercise_data:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return schemas.Exercise(**exercise_data)

@router.post("", response_model=schemas.Exercise)
async def create_exercise(exercise: schemas.ExerciseCreate, db: aiosqlite.Connection = Depends(get_db)):
    exercise_data = await exercise_service.create_exercise(db, exercise)
    return schemas.Exercise(**exercise_data)

@router.put("/{exercise_id}", response_model=schemas.Exercise)
async def update_exercise(exercise_id: int, exercise: schemas.ExerciseCreate, db: aiosqlite.Connection = Depends(get_db)):
    exercise_data = await exercise_service.update_exercise(db, exercise_id, exercise)
    if not exercise_data:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return schemas.Exercise(**exercise_data)

@router.delete("/{exercise_id}")
async def delete_exercise(exercise_id: int, db: aiosqlite.Connection = Depends(get_db)):
    success = await exercise_service.delete_exercise(db, exercise_id)
    if not success:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return {"message": "Exercise deleted successfully"}

@router.post("/{exercise_id}/check")
async def check_answer(exercise_id: int, answer: schemas.ExerciseAnswer, db: aiosqlite.Connection = Depends(get_db)):
    is_correct, explanation = await exercise_service.check_answer(db, exercise_id, answer.user_answer)
    return {
        "is_correct": is_correct,
        "explanation": explanation,
        "exercise_id": exercise_id
    }
