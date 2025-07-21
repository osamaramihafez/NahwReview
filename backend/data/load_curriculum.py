import asyncio
import aiosqlite
import json
import os

async def load_curriculum_from_json(json_file_path="curriculum_data.json"):
    """Load curriculum data from JSON file and populate the database"""
    
    # Check if JSON file exists
    if not os.path.exists(json_file_path):
        print(f"❌ JSON file not found: {json_file_path}")
        return
    
    # Load JSON data
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            curriculum_data = json.load(file)
        print(f"✅ Successfully loaded JSON data from {json_file_path}")
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON file: {e}")
        return
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        return

    async with aiosqlite.connect("nahw_exercises.db") as db:
        
        # Clear existing data
        print("🗑️  Clearing existing database data...")
        await db.execute("DELETE FROM exercises")
        await db.execute("DELETE FROM lessons")
        await db.execute("DELETE FROM levels")
        await db.commit()
        
        # Insert levels
        print("📚 Inserting levels...")
        for level in curriculum_data["levels"]:
            await db.execute(
                """INSERT OR REPLACE INTO levels (id, name, arabic_name, description, arabic_description, "order") 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (level["id"], level["name"], level["arabic_name"], 
                 level["description"], level["arabic_description"], level["order"])
            )
        print(f"✅ Added {len(curriculum_data['levels'])} levels")
        
        # Insert lessons
        print("📖 Inserting lessons...")
        for lesson in curriculum_data["lessons"]:
            await db.execute(
                """INSERT OR REPLACE INTO lessons (id, title, arabic_title, description, arabic_description, "order", level_id) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (lesson["id"], lesson["title"], lesson["arabic_title"], 
                 lesson["description"], lesson["arabic_description"], lesson["order"], lesson["level_id"])
            )
        print(f"✅ Added {len(curriculum_data['lessons'])} lessons")
        
        # Insert exercises
        print("📝 Inserting exercises...")
        for exercise in curriculum_data["exercises"]:
            # Convert the data structure to JSON for storage
            correct_answer_json = json.dumps(exercise["data"], ensure_ascii=False)
            
            # Insert the exercise
            cursor = await db.execute(
                """INSERT INTO exercises 
                   (question, question_arabic, exercise_type, correct_answer, explanation, arabic_explanation, "order", lesson_id) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    exercise["question"],
                    exercise["question_arabic"],
                    exercise["exercise_type"],
                    correct_answer_json,
                    exercise["explanation"],
                    exercise["arabic_explanation"],
                    exercise["order"],
                    exercise["lesson_id"]
                )
            )
            
            print(f"   Added exercise: {exercise['question'][:50]}... (Lesson {exercise['lesson_id']})")
        
        await db.commit()
        print(f"✅ Successfully added {len(curriculum_data['exercises'])} exercises!")

async def show_curriculum_summary():
    """Show the curriculum summary from database"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        db.row_factory = aiosqlite.Row
        
        # Show levels
        cursor = await db.execute("SELECT * FROM levels ORDER BY \"order\"")
        levels = await cursor.fetchall()
        
        print(f"\n=== CURRICULUM SUMMARY ===")
        print(f"Total levels: {len(levels)}")
        print("-" * 80)
        
        for level in levels:
            print(f"Level {level['id']}: {level['name']}")
            print(f"  Arabic: {level['arabic_name']}")
            print(f"  Description: {level['description']}")
            
            # Show lessons for this level
            lesson_cursor = await db.execute(
                "SELECT * FROM lessons WHERE level_id = ? ORDER BY \"order\"", 
                (level['id'],)
            )
            lessons = await lesson_cursor.fetchall()
            
            for lesson in lessons:
                print(f"  └── Lesson {lesson['id']}: {lesson['title']}")
                print(f"      Arabic: {lesson['arabic_title']}")
                
                # Count exercises for this lesson
                ex_cursor = await db.execute(
                    "SELECT COUNT(*) as count FROM exercises WHERE lesson_id = ?", 
                    (lesson['id'],)
                )
                exercise_count = (await ex_cursor.fetchone())['count']
                print(f"      └── {exercise_count} exercises")
            print()
        
        # Show total exercise count
        total_cursor = await db.execute("SELECT COUNT(*) as total FROM exercises")
        total_exercises = (await total_cursor.fetchone())['total']
        print(f"Total exercises: {total_exercises}")

async def main():
    """Main function to load curriculum from JSON and show summary"""
    print("🚀 Loading curriculum from JSON file...")
    print("=" * 60)
    
    await load_curriculum_from_json()
    await show_curriculum_summary()
    
    print("\n✅ Curriculum loading complete!")

if __name__ == "__main__":
    asyncio.run(main())
