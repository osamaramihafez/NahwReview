import asyncio
import aiosqlite
import json

async def show_english_primary_curriculum():
    """Show the English-primary curriculum structure"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        db.row_factory = aiosqlite.Row
        
        print("=== ENGLISH-PRIMARY IRAB CURRICULUM ===")
        print("=" * 50)
        
        # Get levels
        level_cursor = await db.execute("SELECT * FROM levels ORDER BY \"order\"")
        levels = await level_cursor.fetchall()
        
        total_lessons = 0
        total_exercises = 0
        
        for level in levels:
            print(f"\n🎯 {level['name']}")
            print(f"   Arabic: {level['arabic_name']}")
            print(f"   Description: {level['description']}")
            print(f"   Arabic Description: {level['arabic_description']}")
            print("   " + "-" * 60)
            
            # Get lessons for this level
            lesson_cursor = await db.execute(
                """SELECT l.*, COUNT(e.id) as exercise_count 
                   FROM lessons l 
                   LEFT JOIN exercises e ON l.id = e.lesson_id 
                   WHERE l.level_id = ? 
                   GROUP BY l.id 
                   ORDER BY l."order\"""",
                (level['id'],)
            )
            lessons = await lesson_cursor.fetchall()
            
            for lesson in lessons:
                total_lessons += 1
                total_exercises += lesson['exercise_count']
                print(f"   📚 Lesson {lesson['id']}: {lesson['title']}")
                print(f"      Arabic: {lesson['arabic_title']}")
                print(f"      Description: {lesson['description']}")
                print(f"      Arabic Description: {lesson['arabic_description']}")
                print(f"      ✅ {lesson['exercise_count']} exercises")
                
                # Show sample exercise for this lesson
                sample_cursor = await db.execute(
                    "SELECT question, question_arabic FROM exercises WHERE lesson_id = ? LIMIT 1",
                    (lesson['id'],)
                )
                sample = await sample_cursor.fetchone()
                if sample:
                    print(f"      📝 Sample Question: {sample['question']}")
                    print(f"      📝 Arabic: {sample['question_arabic']}")
                print()
        
        print("=" * 50)
        print(f"📊 CURRICULUM STATISTICS:")
        print(f"   • {len(levels)} levels")
        print(f"   • {total_lessons} lessons") 
        print(f"   • {total_exercises} comprehensive exercises")
        if total_lessons > 0:
            print(f"   • Average {total_exercises/total_lessons:.1f} exercises per lesson")
        print("=" * 50)

async def show_exercise_structure():
    """Show detailed structure of exercise questions"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        db.row_factory = aiosqlite.Row
        
        print("\n🔍 EXERCISE QUESTION STRUCTURE:")
        print("-" * 70)
        
        cursor = await db.execute(
            """SELECT e.id, e.question, e.question_arabic, e.explanation, e.arabic_explanation, 
                      e.correct_answer, l.title as lesson_title
               FROM exercises e 
               JOIN lessons l ON e.lesson_id = l.id 
               ORDER BY e.lesson_id, e."order" 
               LIMIT 2"""
        )
        exercises = await cursor.fetchall()
        
        for exercise in exercises:
            print(f"Exercise {exercise['id']} - {exercise['lesson_title']}")
            print(f"  English Question: {exercise['question']}")
            print(f"  Arabic Question: {exercise['question_arabic']}")
            print(f"  English Explanation: {exercise['explanation']}")
            print(f"  Arabic Explanation: {exercise['arabic_explanation']}")
            
            # Parse and show question structure
            try:
                data = json.loads(exercise['correct_answer'])
                if 'words' in data and data['words']:
                    first_word = data['words'][0]
                    if 'questions' in first_word and first_word['questions']:
                        first_q = first_word['questions'][0]
                        print(f"  Sample Word Question (English): {first_q.get('question', 'N/A')}")
                        print(f"  Sample Word Question (Arabic): {first_q.get('question_arabic', 'N/A')}")
                        print(f"  Options (English): {first_q.get('options', [])}")
                        print(f"  Options (Arabic): {first_q.get('options_arabic', [])}")
            except:
                print("  (Could not parse question structure)")
            print()

if __name__ == "__main__":
    asyncio.run(show_english_primary_curriculum())
    asyncio.run(show_exercise_structure())
