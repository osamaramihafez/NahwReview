import asyncio
import aiosqlite

async def check_database_status():
    """Check current database status"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        
        print("📊 DATABASE STATUS CHECK")
        print("=" * 30)
        
        # Check what tables exist
        cursor = await db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = await cursor.fetchall()
        print(f"Existing tables: {[t[0] for t in tables]}")
        
        # Check exercise_options count
        try:
            cursor = await db.execute("SELECT COUNT(*) FROM exercise_options")
            count = await cursor.fetchone()
            print(f"Exercise options count: {count[0]}")
        except:
            print("No exercise_options table found")
        
        # Check if translation tables exist
        try:
            cursor = await db.execute("SELECT COUNT(*) FROM translation_keys")
            count = await cursor.fetchone()
            print(f"Translation keys count: {count[0]}")
        except:
            print("No translation_keys table found")
        
        try:
            cursor = await db.execute("SELECT COUNT(*) FROM translations")
            count = await cursor.fetchone()
            print(f"Translations count: {count[0]}")
        except:
            print("No translations table found")
        
        # Check exercises count
        try:
            cursor = await db.execute("SELECT COUNT(*) FROM exercises")
            count = await cursor.fetchone()
            print(f"Exercises count: {count[0]}")
        except:
            print("No exercises table found")

if __name__ == "__main__":
    asyncio.run(check_database_status())
