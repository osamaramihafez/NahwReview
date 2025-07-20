import asyncio
import aiosqlite

async def show_clean_curriculum_summary():
    """Show summary of the clean irab curriculum"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        db.row_factory = aiosqlite.Row
        
        print("=== CLEAN IRAB CURRICULUM SUMMARY ===")
        print("=" * 50)
        
        # Get levels
        level_cursor = await db.execute("SELECT * FROM levels ORDER BY \"order\"")
        levels = await level_cursor.fetchall()
        
        total_lessons = 0
        total_exercises = 0
        
        for level in levels:
            print(f"\n🎯 {level['name']}")
            print(f"   {level['description']}")
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
                print(f"   📚 Lesson {lesson['id']}: {lesson['arabic_title']}")
                print(f"      {lesson['description']}")
                print(f"      ✅ {lesson['exercise_count']} irab analysis exercises")
                
                # Show sample exercise for this lesson
                sample_cursor = await db.execute(
                    "SELECT question_arabic FROM exercises WHERE lesson_id = ? LIMIT 1",
                    (lesson['id'],)
                )
                sample = await sample_cursor.fetchone()
                if sample:
                    print(f"      📝 Sample: {sample['question_arabic']}")
                print()
        
        print("=" * 50)
        print(f"📊 CURRICULUM STATISTICS:")
        print(f"   • {len(levels)} levels")
        print(f"   • {total_lessons} lessons") 
        print(f"   • {total_exercises} comprehensive irab exercises")
        print(f"   • Average {total_exercises/total_lessons:.1f} exercises per lesson")
        print("=" * 50)

async def show_exercise_details():
    """Show detailed breakdown of exercises by type and lesson"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        db.row_factory = aiosqlite.Row
        
        print("\n🔍 EXERCISE BREAKDOWN BY LESSON:")
        print("-" * 70)
        
        cursor = await db.execute(
            """SELECT l.id, l.arabic_title, l.level_id, COUNT(e.id) as count,
                      GROUP_CONCAT(e.question_arabic, ' | ') as questions
               FROM lessons l 
               LEFT JOIN exercises e ON l.id = e.lesson_id 
               GROUP BY l.id 
               ORDER BY l.level_id, l."order\""""
        )
        lessons = await cursor.fetchall()
        
        for lesson in lessons:
            print(f"Lesson {lesson['id']} (Level {lesson['level_id']}): {lesson['arabic_title']}")
            print(f"  └── {lesson['count']} exercises")
            if lesson['questions']:
                questions = lesson['questions'].split(' | ')
                for i, q in enumerate(questions, 1):
                    print(f"      {i}. {q}")
            print()

if __name__ == "__main__":
    asyncio.run(show_clean_curriculum_summary())
    asyncio.run(show_exercise_details())
