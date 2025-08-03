import aiosqlite
from typing import List, Dict, Any, Optional
import data.schemas as schemas

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

async def update_lesson(db: aiosqlite.Connection, lesson_id: int, lesson: schemas.LessonCreate) -> Optional[Dict[str, Any]]:
    """Update an existing lesson"""
    async with db.execute(
        "UPDATE lessons SET title = ?, arabic_title = ?, description = ?, \"order\" = ?, level_id = ? WHERE id = ?",
        (lesson.title, lesson.arabic_title, lesson.description, lesson.order, lesson.level_id, lesson_id)
    ) as cursor:
        await db.commit()
        if cursor.rowcount == 0:
            return None
        
        # Return the updated lesson
        return await get_lesson_by_id(db, lesson_id)

async def delete_lesson(db: aiosqlite.Connection, lesson_id: int) -> bool:
    """Delete a lesson and all its associated exercises"""
    try:
        # Delete exercise options first
        await db.execute(
            "DELETE FROM exercise_options WHERE exercise_id IN (SELECT id FROM exercises WHERE lesson_id = ?)",
            (lesson_id,)
        )
        
        # Delete exercises
        await db.execute("DELETE FROM exercises WHERE lesson_id = ?", (lesson_id,))
        
        # Delete the lesson
        async with db.execute("DELETE FROM lessons WHERE id = ?", (lesson_id,)) as cursor:
            await db.commit()
            return cursor.rowcount > 0
    except Exception:
        await db.rollback()
        return False

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
