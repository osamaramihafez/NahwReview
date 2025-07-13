import asyncio
import aiosqlite

async def clear_database():
    """Clear all data from the database"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        # Clear all tables in correct order (respecting foreign keys)
        await db.execute("DELETE FROM exercise_options")
        await db.execute("DELETE FROM exercises")
        await db.execute("DELETE FROM user_progress")
        await db.execute("DELETE FROM lessons")
        await db.execute("DELETE FROM levels")
        
        # Add order column to exercises table if it doesn't exist
        try:
            await db.execute("ALTER TABLE exercises ADD COLUMN \"order\" INTEGER DEFAULT 0")
        except:
            pass  # Column might already exist
            
        await db.commit()
        print("Database cleared successfully!")

if __name__ == "__main__":
    asyncio.run(clear_database())
