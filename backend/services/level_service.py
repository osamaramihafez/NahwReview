import aiosqlite
from typing import List, Dict, Any, Optional
import schemas

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
