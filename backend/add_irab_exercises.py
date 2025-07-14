import asyncio
import aiosqlite
import json

# Sample irab analysis exercises
IRAB_ANALYSIS_EXERCISES = [
    {
        "question": "حلل الجملة التالية نحوياً",
        "question_arabic": "ضرب عمرُ أحمدا",
        "exercise_type": "irab_analysis",
        "lesson_id": 1,  # Basic Nouns lesson
        "order": 10,
        "explanation": "هذه جملة فعلية تتكون من فعل وفاعل ومفعول به",
        "data": {
            "sentence": "ضرب عمرُ أحمدا",
            "words": [
                {"text": "ضرب", "position": 0},
                {"text": "عمرُ", "position": 1},
                {"text": "أحمدا", "position": 2}
            ],
            "questions": [
                {
                    "question": "ما نوع الكلمة؟",
                    "options": ["اسم", "فعل", "حرف"],
                    "correct_answer": "فعل",
                    "explanation": "ضرب فعل ماض"
                },
                {
                    "question": "ما حالة الإعراب؟",
                    "options": ["مرفوع", "منصوب", "مجرور", "مجزوم"],
                    "correct_answer": "مجزوم",
                    "explanation": "الفعل الماضي مبني على الفتح"
                }
            ],
            "word_analysis": {
                "0": {  # ضرب
                    "word_type": "فعل",
                    "irab_case": "مبني",
                    "detailed_analysis": "فعل ماض مبني على الفتح لا محل له من الإعراب"
                },
                "1": {  # عمرُ
                    "word_type": "اسم",
                    "irab_case": "مرفوع",
                    "detailed_analysis": "فاعل مرفوع وعلامة رفعه الضمة الظاهرة"
                },
                "2": {  # أحمدا
                    "word_type": "اسم",
                    "irab_case": "منصوب",
                    "detailed_analysis": "مفعول به منصوب وعلامة نصبه الفتحة الظاهرة"
                }
            }
        }
    },
    {
        "question": "حلل الجملة التالية نحوياً",
        "question_arabic": "يكتب الطالبُ الدرسَ",
        "exercise_type": "irab_analysis",
        "lesson_id": 2,  # Basic Verbs lesson
        "order": 5,
        "explanation": "هذه جملة فعلية تتكون من فعل مضارع وفاعل ومفعول به",
        "data": {
            "sentence": "يكتب الطالبُ الدرسَ",
            "words": [
                {"text": "يكتب", "position": 0},
                {"text": "الطالبُ", "position": 1},
                {"text": "الدرسَ", "position": 2}
            ],
            "questions": [
                {
                    "question": "ما نوع الكلمة؟",
                    "options": ["اسم", "فعل", "حرف"],
                    "correct_answer": "فعل",
                    "explanation": "يكتب فعل مضارع"
                },
                {
                    "question": "ما حالة الإعراب؟",
                    "options": ["مرفوع", "منصوب", "مجرور", "مجزوم"],
                    "correct_answer": "مرفوع",
                    "explanation": "الفعل المضارع مرفوع بالضمة"
                }
            ]
        }
    },
    {
        "question": "حلل الجملة التالية نحوياً",
        "question_arabic": "في البيتِ كتابٌ",
        "exercise_type": "irab_analysis",
        "lesson_id": 3,  # Basic Particles lesson
        "order": 8,
        "explanation": "هذه جملة اسمية مقدم فيها الخبر على المبتدأ",
        "data": {
            "sentence": "في البيتِ كتابٌ",
            "words": [
                {"text": "في", "position": 0},
                {"text": "البيتِ", "position": 1},
                {"text": "كتابٌ", "position": 2}
            ],
            "questions": [
                {
                    "question": "ما نوع الكلمة؟",
                    "options": ["اسم", "فعل", "حرف"],
                    "correct_answer": "حرف",
                    "explanation": "في حرف جر"
                },
                {
                    "question": "ما حالة الإعراب؟",
                    "options": ["مرفوع", "منصوب", "مجرور", "مجزوم"],
                    "correct_answer": "مجرور",
                    "explanation": "حرف الجر مبني لا محل له من الإعراب"
                }
            ]
        }
    }
]

async def add_irab_analysis_exercises():
    """Add irab analysis exercises to the database"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        for exercise_data in IRAB_ANALYSIS_EXERCISES:
            # Convert the data structure to JSON for storage
            correct_answer_json = json.dumps(exercise_data["data"], ensure_ascii=False)
            
            # Insert the exercise
            cursor = await db.execute(
                """INSERT INTO exercises 
                   (question, question_arabic, exercise_type, correct_answer, explanation, "order", lesson_id) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    exercise_data["question"],
                    exercise_data["question_arabic"],
                    exercise_data["exercise_type"],
                    correct_answer_json,
                    exercise_data["explanation"],
                    exercise_data["order"],
                    exercise_data["lesson_id"]
                )
            )
            
            exercise_id = cursor.lastrowid
            print(f"Added irab analysis exercise: {exercise_data['question_arabic']} (ID: {exercise_id})")
        
        await db.commit()
        print(f"Successfully added {len(IRAB_ANALYSIS_EXERCISES)} irab analysis exercises!")

async def show_exercises():
    """Show all exercises in the database"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        db.row_factory = aiosqlite.Row
        
        cursor = await db.execute(
            "SELECT id, question_arabic, exercise_type, lesson_id FROM exercises ORDER BY lesson_id, \"order\""
        )
        exercises = await cursor.fetchall()
        
        print(f"\nAll exercises in database ({len(exercises)} total):")
        print("-" * 80)
        for exercise in exercises:
            print(f"ID: {exercise['id']:<3} | Type: {exercise['exercise_type']:<15} | Lesson: {exercise['lesson_id']:<2} | Question: {exercise['question_arabic']}")

if __name__ == "__main__":
    print("Adding irab analysis exercises...")
    asyncio.run(add_irab_analysis_exercises())
    asyncio.run(show_exercises())
