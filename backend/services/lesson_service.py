import aiosqlite
from typing import List, Dict, Any, Optional
import schemas

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
