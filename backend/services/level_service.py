import aiosqlite
from typing import List, Dict, Any, Optional
import data.schemas as schemas

async def get_all_levels(db: aiosqlite.Connection) -> List[Dict[str, Any]]:
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

async def update_level(db: aiosqlite.Connection, level_id: int, level: schemas.LevelCreate) -> Optional[Dict[str, Any]]:
    """Update an existing level"""
    async with db.execute(
        "UPDATE levels SET name = ?, description = ?, \"order\" = ? WHERE id = ?",
        (level.name, level.description, level.order, level_id)
    ) as cursor:
        await db.commit()
        if cursor.rowcount == 0:
            return None
        
        # Return the updated level
        return await get_level_by_id(db, level_id)

async def delete_level(db: aiosqlite.Connection, level_id: int) -> bool:
    """Delete a level and all its associated lessons and exercises"""
    try:
        # Delete exercises first (they reference lessons)
        await db.execute(
            "DELETE FROM exercise_options WHERE exercise_id IN (SELECT e.id FROM exercises e JOIN lessons l ON e.lesson_id = l.id WHERE l.level_id = ?)",
            (level_id,)
        )
        await db.execute(
            "DELETE FROM exercises WHERE lesson_id IN (SELECT id FROM lessons WHERE level_id = ?)",
            (level_id,)
        )
        
        # Delete lessons
        await db.execute("DELETE FROM lessons WHERE level_id = ?", (level_id,))
        
        # Delete the level
        async with db.execute("DELETE FROM levels WHERE id = ?", (level_id,)) as cursor:
            await db.commit()
            return cursor.rowcount > 0
    except Exception:
        await db.rollback()
        return False

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
