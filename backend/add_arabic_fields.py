import asyncio
import aiosqlite

async def add_arabic_fields():
    """Add Arabic fields to existing tables"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        try:
            # Add Arabic name field to levels table
            await db.execute("ALTER TABLE levels ADD COLUMN arabic_name TEXT")
            print("Added arabic_name field to levels table")
        except Exception as e:
            print(f"arabic_name field may already exist in levels: {e}")
        
        try:
            # Add Arabic description field to levels table
            await db.execute("ALTER TABLE levels ADD COLUMN arabic_description TEXT")
            print("Added arabic_description field to levels table")
        except Exception as e:
            print(f"arabic_description field may already exist in levels: {e}")
        
        try:
            # Add Arabic description field to lessons table
            await db.execute("ALTER TABLE lessons ADD COLUMN arabic_description TEXT")
            print("Added arabic_description field to lessons table")
        except Exception as e:
            print(f"arabic_description field may already exist in lessons: {e}")
        
        try:
            # Add Arabic explanation field to exercises table
            await db.execute("ALTER TABLE exercises ADD COLUMN arabic_explanation TEXT")
            print("Added arabic_explanation field to exercises table")
        except Exception as e:
            print(f"arabic_explanation field may already exist in exercises: {e}")
        
        await db.commit()
        print("Database schema updated successfully!")

if __name__ == "__main__":
    asyncio.run(add_arabic_fields())
