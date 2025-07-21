import aiosqlite
from typing import List, Dict, Any, Optional, Tuple
import schemas

async def get_exercises_by_lesson(db: aiosqlite.Connection, lesson_id: int) -> List[Dict[str, Any]]:
    """Get all exercises for a lesson ordered by order"""
    async with db.execute(
        "SELECT * FROM exercises WHERE lesson_id = ? ORDER BY \"order\"",
        (lesson_id,)
    ) as cursor:
        rows = await cursor.fetchall()
        exercises = [dict(row) for row in rows]
        
        # Get options for each exercise
        for exercise in exercises:
            exercise['options'] = await get_exercise_options(db, exercise['id'])
        
        return exercises

async def get_exercise_options(db: aiosqlite.Connection, exercise_id: int) -> List[Dict[str, Any]]:
    """Get all options for an exercise"""
    async with db.execute(
        "SELECT * FROM exercise_options WHERE exercise_id = ?",
        (exercise_id,)
    ) as cursor:
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def get_exercise_by_id(db: aiosqlite.Connection, exercise_id: int) -> Optional[Dict[str, Any]]:
    """Get exercise by ID with options"""
    async with db.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,)) as cursor:
        row = await cursor.fetchone()
        if row:
            exercise = dict(row)
            exercise['options'] = await get_exercise_options(db, exercise_id)
            return exercise
        return None

async def create_exercise(db: aiosqlite.Connection, exercise: schemas.ExerciseCreate) -> Dict[str, Any]:
    """Create a new exercise with options"""
    async with db.execute(
        "INSERT INTO exercises (question, question_arabic, exercise_type, correct_answer, explanation, \"order\", lesson_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (exercise.question, exercise.question_arabic, exercise.exercise_type, exercise.correct_answer, exercise.explanation, getattr(exercise, 'order', 0), exercise.lesson_id)
    ) as cursor:
        exercise_id = cursor.lastrowid
        
        # Add options
        for option in exercise.options:
            await db.execute(
                "INSERT INTO exercise_options (option_text, is_correct, exercise_id) VALUES (?, ?, ?)",
                (option.option_text, option.is_correct, exercise_id)
            )
        
        await db.commit()
        
        # Return the created exercise
        return await get_exercise_by_id(db, exercise_id)

async def check_answer(db: aiosqlite.Connection, exercise_id: int, user_answer: str) -> Tuple[bool, str]:
    """Check if user answer is correct"""
    exercise = await get_exercise_by_id(db, exercise_id)
    if not exercise:
        return False, "Exercise not found"
    
    # Handle different exercise types
    if exercise['exercise_type'] == 'irab_analysis':
        # For irab analysis, we consider the exercise complete when user_answer contains completion message
        is_correct = "تم إكمال التحليل النحوي بنجاح" in user_answer
        return is_correct, exercise['explanation'] or ""
    else:
        # Traditional answer checking for multiple choice and other types
        is_correct = exercise['correct_answer'].lower().strip() == user_answer.lower().strip()
        return is_correct, exercise['explanation'] or ""
