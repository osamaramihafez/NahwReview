import asyncio
import aiosqlite

async def check_database():
    async with aiosqlite.connect("nahw_exercises.db") as db:
        db.row_factory = aiosqlite.Row
        
        # Check lessons
        cursor = await db.execute("SELECT * FROM lessons WHERE id <= 3")
        lessons = await cursor.fetchall()
        print("Lessons found:")
        for lesson in lessons:
            print(f"  ID: {lesson['id']}, Title: {lesson['title']}, Level: {lesson['level_id']}")
        
        # Check exercises for lesson 1
        cursor = await db.execute("SELECT * FROM exercises WHERE lesson_id = 1")
        exercises = await cursor.fetchall()
        print(f"\nExercises in lesson 1: {len(exercises)}")
        for exercise in exercises:
            print(f"  ID: {exercise['id']}, Type: {exercise['exercise_type']}, Question: {exercise['question_arabic']}")

if __name__ == "__main__":
    asyncio.run(check_database())
