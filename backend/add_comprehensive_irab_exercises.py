import asyncio
import aiosqlite
import json

# More comprehensive irab analysis exercises
COMPREHENSIVE_IRAB_EXERCISES = [
    {
        "question": "حلل الجملة التالية نحوياً كلمة كلمة",
        "question_arabic": "ضرب عمرُ أحمدا",
        "exercise_type": "irab_analysis",
        "lesson_id": 1,
        "order": 15,
        "explanation": "هذه جملة فعلية تتكون من فعل ماض وفاعل ومفعول به",
        "data": {
            "sentence": "ضرب عمرُ أحمدا",
            "words": [
                {
                    "text": "ضرب",
                    "position": 0,
                    "questions": [
                        {
                            "question": "ما نوع الكلمة 'ضرب'؟",
                            "options": ["اسم", "فعل", "حرف"],
                            "correct_answer": "فعل",
                            "explanation": "ضرب فعل ماض"
                        },
                        {
                            "question": "ما زمن الفعل 'ضرب'؟",
                            "options": ["ماض", "مضارع", "أمر"],
                            "correct_answer": "ماض",
                            "explanation": "ضرب فعل ماض دل على حدث وقع في الزمن الماضي"
                        },
                        {
                            "question": "ما حالة بناء الفعل 'ضرب'؟",
                            "options": ["مبني على الفتح", "مبني على الضم", "مبني على السكون"],
                            "correct_answer": "مبني على الفتح",
                            "explanation": "الفعل الماضي مبني على الفتح"
                        }
                    ]
                },
                {
                    "text": "عمرُ",
                    "position": 1,
                    "questions": [
                        {
                            "question": "ما نوع الكلمة 'عمرُ'؟",
                            "options": ["اسم", "فعل", "حرف"],
                            "correct_answer": "اسم",
                            "explanation": "عمرُ اسم علم"
                        },
                        {
                            "question": "ما موقع 'عمرُ' في الجملة؟",
                            "options": ["فاعل", "مفعول به", "مبتدأ"],
                            "correct_answer": "فاعل",
                            "explanation": "عمرُ فاعل للفعل ضرب"
                        },
                        {
                            "question": "ما حالة إعراب 'عمرُ'؟",
                            "options": ["مرفوع", "منصوب", "مجرور"],
                            "correct_answer": "مرفوع",
                            "explanation": "الفاعل مرفوع دائماً وعلامة رفعه الضمة"
                        }
                    ]
                },
                {
                    "text": "أحمدا",
                    "position": 2,
                    "questions": [
                        {
                            "question": "ما نوع الكلمة 'أحمدا'؟",
                            "options": ["اسم", "فعل", "حرف"],
                            "correct_answer": "اسم",
                            "explanation": "أحمدا اسم علم"
                        },
                        {
                            "question": "ما موقع 'أحمدا' في الجملة؟",
                            "options": ["فاعل", "مفعول به", "خبر"],
                            "correct_answer": "مفعول به",
                            "explanation": "أحمدا مفعول به للفعل ضرب"
                        },
                        {
                            "question": "ما حالة إعراب 'أحمدا'؟",
                            "options": ["مرفوع", "منصوب", "مجرور"],
                            "correct_answer": "منصوب",
                            "explanation": "المفعول به منصوب دائماً وعلامة نصبه الفتحة"
                        }
                    ]
                }
            ]
        }
    },
    {
        "question": "حلل الجملة التالية نحوياً كلمة كلمة",
        "question_arabic": "يكتب الطالبُ الدرسَ",
        "exercise_type": "irab_analysis",
        "lesson_id": 2,
        "order": 10,
        "explanation": "هذه جملة فعلية تتكون من فعل مضارع وفاعل ومفعول به",
        "data": {
            "sentence": "يكتب الطالبُ الدرسَ",
            "words": [
                {
                    "text": "يكتب",
                    "position": 0,
                    "questions": [
                        {
                            "question": "ما نوع الكلمة 'يكتب'؟",
                            "options": ["اسم", "فعل", "حرف"],
                            "correct_answer": "فعل",
                            "explanation": "يكتب فعل مضارع"
                        },
                        {
                            "question": "ما زمن الفعل 'يكتب'؟",
                            "options": ["ماض", "مضارع", "أمر"],
                            "correct_answer": "مضارع",
                            "explanation": "يكتب فعل مضارع يدل على الحال أو الاستقبال"
                        },
                        {
                            "question": "ما حالة إعراب 'يكتب'؟",
                            "options": ["مرفوع", "منصوب", "مجزوم"],
                            "correct_answer": "مرفوع",
                            "explanation": "الفعل المضارع مرفوع بالضمة لعدم دخول ناصب أو جازم عليه"
                        }
                    ]
                },
                {
                    "text": "الطالبُ",
                    "position": 1,
                    "questions": [
                        {
                            "question": "ما نوع الكلمة 'الطالبُ'؟",
                            "options": ["اسم", "فعل", "حرف"],
                            "correct_answer": "اسم",
                            "explanation": "الطالبُ اسم"
                        },
                        {
                            "question": "ما موقع 'الطالبُ' في الجملة؟",
                            "options": ["فاعل", "مفعول به", "مبتدأ"],
                            "correct_answer": "فاعل",
                            "explanation": "الطالبُ فاعل للفعل يكتب"
                        },
                        {
                            "question": "ما حالة إعراب 'الطالبُ'؟",
                            "options": ["مرفوع", "منصوب", "مجرور"],
                            "correct_answer": "مرفوع",
                            "explanation": "الفاعل مرفوع وعلامة رفعه الضمة الظاهرة"
                        }
                    ]
                },
                {
                    "text": "الدرسَ",
                    "position": 2,
                    "questions": [
                        {
                            "question": "ما نوع الكلمة 'الدرسَ'؟",
                            "options": ["اسم", "فعل", "حرف"],
                            "correct_answer": "اسم",
                            "explanation": "الدرسَ اسم"
                        },
                        {
                            "question": "ما موقع 'الدرسَ' في الجملة؟",
                            "options": ["فاعل", "مفعول به", "خبر"],
                            "correct_answer": "مفعول به",
                            "explanation": "الدرسَ مفعول به للفعل يكتب"
                        },
                        {
                            "question": "ما حالة إعراب 'الدرسَ'؟",
                            "options": ["مرفوع", "منصوب", "مجرور"],
                            "correct_answer": "منصوب",
                            "explanation": "المفعول به منصوب وعلامة نصبه الفتحة الظاهرة"
                        }
                    ]
                }
            ]
        }
    }
]

async def clear_existing_irab_exercises():
    """Remove existing irab analysis exercises"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        await db.execute("DELETE FROM exercises WHERE exercise_type = 'irab_analysis'")
        await db.commit()
        print("Cleared existing irab analysis exercises")

async def add_comprehensive_irab_exercises():
    """Add comprehensive irab analysis exercises to the database"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        for exercise_data in COMPREHENSIVE_IRAB_EXERCISES:
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
            print(f"Added comprehensive irab analysis exercise: {exercise_data['question_arabic']} (ID: {exercise_id})")
        
        await db.commit()
        print(f"Successfully added {len(COMPREHENSIVE_IRAB_EXERCISES)} comprehensive irab analysis exercises!")

async def show_irab_exercises():
    """Show all irab analysis exercises in the database"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        db.row_factory = aiosqlite.Row
        
        cursor = await db.execute(
            "SELECT id, question_arabic, exercise_type, lesson_id FROM exercises WHERE exercise_type = 'irab_analysis' ORDER BY lesson_id, \"order\""
        )
        exercises = await cursor.fetchall()
        
        print(f"\nIrab Analysis exercises in database ({len(exercises)} total):")
        print("-" * 80)
        for exercise in exercises:
            print(f"ID: {exercise['id']:<3} | Lesson: {exercise['lesson_id']:<2} | Question: {exercise['question_arabic']}")

if __name__ == "__main__":
    print("Updating irab analysis exercises...")
    asyncio.run(clear_existing_irab_exercises())
    asyncio.run(add_comprehensive_irab_exercises())
    asyncio.run(show_irab_exercises())
