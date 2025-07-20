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
        
        # Create translation system tables
        await db.execute("""
            CREATE TABLE translation_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_name TEXT UNIQUE NOT NULL,
                category TEXT,
                description TEXT
            )
        """)
        
        await db.execute("""
            CREATE TABLE translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                translation_key_id INTEGER NOT NULL,
                language_code TEXT NOT NULL,
                text TEXT NOT NULL,
                is_primary BOOLEAN DEFAULT 0,
                FOREIGN KEY (translation_key_id) REFERENCES translation_keys (id),
                UNIQUE(translation_key_id, language_code, text)
            )
        """)
        
        # Create exercise_options table with translation support
        await db.execute("""
            CREATE TABLE exercise_options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                translation_key_id INTEGER,
                option_text TEXT,
                is_correct BOOLEAN DEFAULT 0,
                exercise_id INTEGER NOT NULL,
                FOREIGN KEY (translation_key_id) REFERENCES translation_keys (id),
                FOREIGN KEY (exercise_id) REFERENCES exercises (id)
            )
        """)
        
        # Create user_progress table
        await db.execute("""
            CREATE TABLE user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                lesson_id INTEGER NOT NULL,
                completed BOOLEAN DEFAULT 0,
                score INTEGER DEFAULT 0,
                FOREIGN KEY (lesson_id) REFERENCES lessons (id)
            )
        """)
        
        await db.commit()
        print("✅ Database schema updated successfully!")
        print("New schema includes separate fields for English and Arabic content.")

if __name__ == "__main__":
    asyncio.run(update_database_schema())
