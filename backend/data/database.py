import aiosqlite
import asyncio
from typing import AsyncGenerator

DATABASE_URL = "nahw_exercises.db"

async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    async with aiosqlite.connect(DATABASE_URL) as db:
        db.row_factory = aiosqlite.Row
        yield db

async def init_database():
    """Initialize the database with tables"""
    async with aiosqlite.connect(DATABASE_URL) as db:
        # Create levels table with separate English and Arabic fields
        await db.execute("""
            CREATE TABLE IF NOT EXISTS levels (
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
            CREATE TABLE IF NOT EXISTS lessons (
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
            CREATE TABLE IF NOT EXISTS exercises (
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
        
        # Create exercise_options table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS exercise_options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                option_text TEXT NOT NULL,
                is_correct BOOLEAN DEFAULT 0,
                exercise_id INTEGER NOT NULL,
                FOREIGN KEY (exercise_id) REFERENCES exercises (id)
            )
        """)
        
        # Create user_progress table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                lesson_id INTEGER NOT NULL,
                completed BOOLEAN DEFAULT 0,
                score INTEGER DEFAULT 0,
                FOREIGN KEY (lesson_id) REFERENCES lessons (id)
            )
        """)
        
        await db.commit()
