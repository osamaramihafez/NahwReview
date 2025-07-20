import asyncio
import aiosqlite
import json

async def verify_correct_answers():
    """Verify that all exercises have both English and Arabic correct answers"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        db.row_factory = aiosqlite.Row
        
        cursor = await db.execute("SELECT * FROM exercises ORDER BY lesson_id, \"order\"")
        exercises = await cursor.fetchall()
        
        print("=== CORRECT ANSWER VERIFICATION ===")
        print(f"Total exercises: {len(exercises)}")
        print("-" * 60)
        
        for exercise in exercises:
            print(f"Exercise {exercise['id']} (Lesson {exercise['lesson_id']}):")
            print(f"  Question: {exercise['question']}")
            
            # Parse the exercise data
            data = json.loads(exercise['correct_answer'])
            
            missing_arabic_answers = []
            total_questions = 0
            
            for word in data['words']:
                print(f"\n  Word: {word['text']}")
                for q_num, question in enumerate(word['questions'], 1):
                    total_questions += 1
                    has_arabic = 'correct_answer_arabic' in question
                    status = "✅" if has_arabic else "❌"
                    
                    print(f"    Q{q_num}: {status} English: '{question['correct_answer']}'")
                    if has_arabic:
                        print(f"         Arabic: '{question['correct_answer_arabic']}'")
                    else:
                        missing_arabic_answers.append(f"Word '{word['text']}' Q{q_num}")
            
            if missing_arabic_answers:
                print(f"\n  ❌ Missing Arabic answers in: {', '.join(missing_arabic_answers)}")
            else:
                print(f"\n  ✅ All {total_questions} questions have both English and Arabic answers")
            
            print("-" * 40)

if __name__ == "__main__":
    asyncio.run(verify_correct_answers())
