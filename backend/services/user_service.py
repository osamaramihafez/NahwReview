import aiosqlite
from typing import List, Dict, Any, Optional
import schemas

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
