import asyncio
import aiosqlite

async def show_lessons_and_exercises():
    async with aiosqlite.connect('nahw_exercises.db') as db:
        db.row_factory = aiosqlite.Row
        
        # Show lessons
        cursor = await db.execute('SELECT id, title, arabic_title, level_id FROM lessons ORDER BY level_id, "order"')
        lessons = await cursor.fetchall()
        
        print('Available lessons:')
        print('-' * 60)
        for lesson in lessons:
            print(f'ID: {lesson["id"]:<2} | Level: {lesson["level_id"]} | {lesson["title"]} ({lesson["arabic_title"]})')
        
        print('\nExercises in lessons 1 and 2:')
        print('-' * 60)
        
        # Show exercises for lessons 1 and 2
        cursor = await db.execute(
            'SELECT id, question_arabic, exercise_type, lesson_id FROM exercises WHERE lesson_id IN (1, 2) ORDER BY lesson_id, "order"'
        )
        exercises = await cursor.fetchall()
        
        for exercise in exercises:
            print(f'ID: {exercise["id"]:<2} | Lesson: {exercise["lesson_id"]} | Type: {exercise["exercise_type"]:<15} | {exercise["question_arabic"]}')

if __name__ == "__main__":
    asyncio.run(show_lessons_and_exercises())
