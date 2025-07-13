import aiosqlite
from typing import List, Dict, Any, Optional, Tuple
import schemas

async def get_levels(db: aiosqlite.Connection) -> List[Dict[str, Any]]:
    """Get all levels ordered by order"""
    async with db.execute("SELECT * FROM levels ORDER BY \"order\"") as cursor:
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def get_level_by_id(db: aiosqlite.Connection, level_id: int) -> Optional[Dict[str, Any]]:
    """Get level by ID"""
    async with db.execute("SELECT * FROM levels WHERE id = ?", (level_id,)) as cursor:
        row = await cursor.fetchone()
        return dict(row) if row else None

async def create_level(db: aiosqlite.Connection, level: schemas.LevelCreate) -> Dict[str, Any]:
    """Create a new level"""
    async with db.execute(
        "INSERT INTO levels (name, description, \"order\") VALUES (?, ?, ?)",
        (level.name, level.description, level.order)
    ) as cursor:
        level_id = cursor.lastrowid
        await db.commit()
        
        # Return the created level
        return await get_level_by_id(db, level_id)

async def get_lessons_by_level(db: aiosqlite.Connection, level_id: int) -> List[Dict[str, Any]]:
    """Get all lessons for a level ordered by order"""
    async with db.execute(
        "SELECT * FROM lessons WHERE level_id = ? ORDER BY \"order\"",
        (level_id,)
    ) as cursor:
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def get_lesson_by_id(db: aiosqlite.Connection, lesson_id: int) -> Optional[Dict[str, Any]]:
    """Get lesson by ID"""
    async with db.execute("SELECT * FROM lessons WHERE id = ?", (lesson_id,)) as cursor:
        row = await cursor.fetchone()
        return dict(row) if row else None

async def create_lesson(db: aiosqlite.Connection, lesson: schemas.LessonCreate) -> Dict[str, Any]:
    """Create a new lesson"""
    async with db.execute(
        "INSERT INTO lessons (title, arabic_title, description, \"order\", level_id) VALUES (?, ?, ?, ?, ?)",
        (lesson.title, lesson.arabic_title, lesson.description, lesson.order, lesson.level_id)
    ) as cursor:
        lesson_id = cursor.lastrowid
        await db.commit()
        
        # Return the created lesson
        return await get_lesson_by_id(db, lesson_id)

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
    
    is_correct = exercise['correct_answer'].lower().strip() == user_answer.lower().strip()
    return is_correct, exercise['explanation'] or ""

async def get_user_progress(db: aiosqlite.Connection, user_id: str) -> List[Dict[str, Any]]:
    """Get user progress for all lessons"""
    async with db.execute(
        "SELECT * FROM user_progress WHERE user_id = ?",
        (user_id,)
    ) as cursor:
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def update_user_progress(db: aiosqlite.Connection, user_id: str, lesson_id: int, completed: bool, score: int) -> Dict[str, Any]:
    """Update or create user progress"""
    # Check if progress exists
    async with db.execute(
        "SELECT * FROM user_progress WHERE user_id = ? AND lesson_id = ?",
        (user_id, lesson_id)
    ) as cursor:
        existing = await cursor.fetchone()
    
    if existing:
        # Update existing progress
        await db.execute(
            "UPDATE user_progress SET completed = ?, score = ? WHERE user_id = ? AND lesson_id = ?",
            (completed, score, user_id, lesson_id)
        )
        progress_id = existing['id']
    else:
        # Create new progress
        async with db.execute(
            "INSERT INTO user_progress (user_id, lesson_id, completed, score) VALUES (?, ?, ?, ?)",
            (user_id, lesson_id, completed, score)
        ) as cursor:
            progress_id = cursor.lastrowid
    
    await db.commit()
    
    # Return the updated progress
    async with db.execute(
        "SELECT * FROM user_progress WHERE id = ?",
        (progress_id,)
    ) as cursor:
        row = await cursor.fetchone()
        return dict(row) if row else None

async def get_next_lesson(db: aiosqlite.Connection, current_lesson_id: int) -> Optional[Dict[str, Any]]:
    """Get the next lesson in the same level"""
    # First get the current lesson's level and order
    async with db.execute(
        "SELECT level_id, \"order\" FROM lessons WHERE id = ?",
        (current_lesson_id,)
    ) as cursor:
        current_lesson = await cursor.fetchone()
        if not current_lesson:
            return None
    
    # Get the next lesson in the same level
    async with db.execute(
        "SELECT * FROM lessons WHERE level_id = ? AND \"order\" > ? ORDER BY \"order\" LIMIT 1",
        (current_lesson['level_id'], current_lesson['order'])
    ) as cursor:
        row = await cursor.fetchone()
        return dict(row) if row else None

async def get_next_level(db: aiosqlite.Connection, current_level_id: int) -> Optional[Dict[str, Any]]:
    """Get the next level"""
    # First get the current level's order
    async with db.execute(
        "SELECT \"order\" FROM levels WHERE id = ?",
        (current_level_id,)
    ) as cursor:
        current_level = await cursor.fetchone()
        if not current_level:
            return None
    
    # Get the next level
    async with db.execute(
        "SELECT * FROM levels WHERE \"order\" > ? ORDER BY \"order\" LIMIT 1",
        (current_level['order'],)
    ) as cursor:
        row = await cursor.fetchone()
        return dict(row) if row else None
