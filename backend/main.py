from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import aiosqlite
from typing import List
import crud
import schemas
from database import get_db, init_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    await init_database()
    yield

app = FastAPI(
    title="Nahw Exercises API", 
    description="API for Arabic Grammar Learning",
    lifespan=lifespan
)

# Enable CORS for React Native
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Nahw Exercises API"}

@app.get("/levels", response_model=List[schemas.Level])
async def get_levels(db: aiosqlite.Connection = Depends(get_db)):
    levels_data = await crud.get_levels(db)
    return [schemas.Level(**level) for level in levels_data]

@app.get("/levels/{level_id}", response_model=schemas.Level)
async def get_level(level_id: int, db: aiosqlite.Connection = Depends(get_db)):
    level_data = await crud.get_level_by_id(db, level_id)
    if not level_data:
        raise HTTPException(status_code=404, detail="Level not found")
    return schemas.Level(**level_data)

@app.post("/levels", response_model=schemas.Level)
async def create_level(level: schemas.LevelCreate, db: aiosqlite.Connection = Depends(get_db)):
    level_data = await crud.create_level(db, level)
    return schemas.Level(**level_data)

@app.get("/levels/{level_id}/lessons", response_model=List[schemas.Lesson])
async def get_lessons_by_level(level_id: int, db: aiosqlite.Connection = Depends(get_db)):
    lessons_data = await crud.get_lessons_by_level(db, level_id)
    return [schemas.Lesson(**lesson) for lesson in lessons_data]

@app.get("/lessons/{lesson_id}", response_model=schemas.Lesson)
async def get_lesson(lesson_id: int, db: aiosqlite.Connection = Depends(get_db)):
    lesson_data = await crud.get_lesson_by_id(db, lesson_id)
    if not lesson_data:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return schemas.Lesson(**lesson_data)

@app.post("/lessons", response_model=schemas.Lesson)
async def create_lesson(lesson: schemas.LessonCreate, db: aiosqlite.Connection = Depends(get_db)):
    lesson_data = await crud.create_lesson(db, lesson)
    return schemas.Lesson(**lesson_data)

@app.get("/lessons/{lesson_id}/exercises", response_model=List[schemas.Exercise])
async def get_exercises_by_lesson(lesson_id: int, db: aiosqlite.Connection = Depends(get_db)):
    exercises_data = await crud.get_exercises_by_lesson(db, lesson_id)
    return [schemas.Exercise(**exercise) for exercise in exercises_data]

@app.get("/exercises/{exercise_id}", response_model=schemas.Exercise)
async def get_exercise(exercise_id: int, db: aiosqlite.Connection = Depends(get_db)):
    exercise_data = await crud.get_exercise_by_id(db, exercise_id)
    if not exercise_data:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return schemas.Exercise(**exercise_data)

@app.post("/exercises", response_model=schemas.Exercise)
async def create_exercise(exercise: schemas.ExerciseCreate, db: aiosqlite.Connection = Depends(get_db)):
    exercise_data = await crud.create_exercise(db, exercise)
    return schemas.Exercise(**exercise_data)

@app.post("/exercises/{exercise_id}/check")
async def check_answer(exercise_id: int, answer: schemas.ExerciseAnswer, db: aiosqlite.Connection = Depends(get_db)):
    is_correct, explanation = await crud.check_answer(db, exercise_id, answer.user_answer)
    return {
        "is_correct": is_correct,
        "explanation": explanation,
        "exercise_id": exercise_id
    }

@app.get("/users/{user_id}/progress", response_model=List[schemas.UserProgress])
async def get_user_progress(user_id: str, db: aiosqlite.Connection = Depends(get_db)):
    progress_data = await crud.get_user_progress(db, user_id)
    return [schemas.UserProgress(**progress) for progress in progress_data]

@app.post("/users/{user_id}/progress", response_model=schemas.UserProgress)
async def update_progress(user_id: str, progress: schemas.UserProgressCreate, db: aiosqlite.Connection = Depends(get_db)):
    progress_data = await crud.update_user_progress(db, user_id, progress.lesson_id, progress.completed, progress.score)
    return schemas.UserProgress(**progress_data)

@app.get("/lessons/{lesson_id}/next", response_model=schemas.Lesson)
async def get_next_lesson(lesson_id: int, db: aiosqlite.Connection = Depends(get_db)):
    """Get the next lesson in the same level"""
    next_lesson_data = await crud.get_next_lesson(db, lesson_id)
    if not next_lesson_data:
        raise HTTPException(status_code=404, detail="No next lesson found")
    return schemas.Lesson(**next_lesson_data)

@app.get("/levels/{level_id}/next", response_model=schemas.Level)
async def get_next_level(level_id: int, db: aiosqlite.Connection = Depends(get_db)):
    """Get the next level"""
    next_level_data = await crud.get_next_level(db, level_id)
    if not next_level_data:
        raise HTTPException(status_code=404, detail="No next level found")
    return schemas.Level(**next_level_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
