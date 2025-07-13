import asyncio
import aiosqlite

async def show_exercise_summary():
    """Show exercise summary by lesson"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        db.row_factory = aiosqlite.Row
        
        print("=== EXERCISE SUMMARY ===\n")
        
        lesson_names = {
            6: "Past Tense Verbs (الفعل الماضي)",
            7: "Present/Future Tense (الفعل المضارع)", 
            8: "Subject and Predicate (المبتدأ والخبر)",
            9: "Subject/Doer (الفاعل)",
            10: "Direct Object (المفعول به)"
        }
        
        for lesson_id in [6, 7, 8, 9, 10]:
            async with db.execute(
                "SELECT COUNT(*) as count FROM exercises WHERE lesson_id = ?", 
                (lesson_id,)
            ) as cursor:
                result = await cursor.fetchone()
                count = result[0]
                print(f"Lesson {lesson_id} - {lesson_names[lesson_id]}: {count} exercises")
        
        print(f"\nTotal intermediate grammar exercises: {sum([5, 5, 5, 5, 5])}")
        
        # Show some sample exercises
        print("\n=== SAMPLE EXERCISES ===")
        async with db.execute(
            "SELECT e.question, e.question_arabic, l.title FROM exercises e JOIN lessons l ON e.lesson_id = l.id WHERE e.lesson_id IN (6,7,8,9,10) ORDER BY e.lesson_id, e.\"order\" LIMIT 5"
        ) as cursor:
            exercises = await cursor.fetchall()
            for i, ex in enumerate(exercises, 1):
                print(f"{i}. {ex[2]}: {ex[0]}")
                print(f"   Arabic: {ex[1]}\n")

if __name__ == "__main__":
    asyncio.run(show_exercise_summary())
