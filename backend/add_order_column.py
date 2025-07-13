import asyncio
import aiosqlite

async def add_order_column():
    """Add order column to exercises table"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        try:
            await db.execute('ALTER TABLE exercises ADD COLUMN "order" INTEGER DEFAULT 0')
            await db.commit()
            print("Added order column to exercises table")
        except Exception as e:
            print(f"Column might already exist: {e}")

if __name__ == "__main__":
    asyncio.run(add_order_column())
