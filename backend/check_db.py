import asyncio
import aiosqlite

async def check_database():
    """Check current database content"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        db.row_factory = aiosqlite.Row
        
        print("=== LEVELS ===")
        async with db.execute('SELECT * FROM levels ORDER BY "order"') as cursor:
            levels = await cursor.fetchall()
            for level in levels:
                print(dict(level))
        
        print("\n=== LESSONS ===")
        async with db.execute('SELECT * FROM lessons ORDER BY level_id, "order"') as cursor:
            lessons = await cursor.fetchall()
            for lesson in lessons:
                print(dict(lesson))
        
        print("\n=== EXERCISES ===")
        async with db.execute('SELECT COUNT(*) as count FROM exercises') as cursor:
            count = await cursor.fetchone()
            print(f"Total exercises: {count['count']}")

if __name__ == "__main__":
    asyncio.run(check_database())
