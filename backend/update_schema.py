import asyncio
import aiosqlite

async def update_database_schema():
    """Update database schema to support separate English and Arabic fields"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        
        # Drop existing tables to recreate with new schema
        print("Dropping existing tables...")
        await db.execute("DROP TABLE IF EXISTS exercises")
        await db.execute("DROP TABLE IF EXISTS lessons") 
        await db.execute("DROP TABLE IF EXISTS levels")
        
        # Create levels table with separate English and Arabic fields
        await db.execute("""
            CREATE TABLE levels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                arabic_name TEXT,
                description TEXT,
                arabic_description TEXT,
                "order" INTEGER NOT NULL
            )
        """)
        
        # Create lessons table with separate English and Arabic fields
        await db.execute("""
            CREATE TABLE lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                arabic_title TEXT,
                description TEXT,
                arabic_description TEXT,
                "order" INTEGER NOT NULL,
                level_id INTEGER NOT NULL,
                FOREIGN KEY (level_id) REFERENCES levels (id)
            )
        """)
        
        # Create exercises table with separate English and Arabic fields
        await db.execute("""
            CREATE TABLE exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                question_arabic TEXT,
                exercise_type TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                explanation TEXT,
                arabic_explanation TEXT,
                "order" INTEGER DEFAULT 0,
                lesson_id INTEGER NOT NULL,
                FOREIGN KEY (lesson_id) REFERENCES lessons (id)
            )
        """)
        
        await db.commit()
        print("✅ Database schema updated successfully!")
        print("New schema includes separate fields for English and Arabic content.")

if __name__ == "__main__":
    asyncio.run(update_database_schema())
