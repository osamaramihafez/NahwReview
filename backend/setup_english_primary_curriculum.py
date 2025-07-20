import asyncio
import aiosqlite
import json
import os

# Clean, focused levels and lessons for irab analysis with separate English/Arabic fields
CLEAN_LEVELS = [
    {
        "id": 1,
        "name": "Level 1 - Basic Sentences",
        "arabic_name": "المستوى الأول - الجمل البسيطة",
        "description": "Learn the fundamentals of analyzing basic verbal and nominal sentences",
        "arabic_description": "تعلم أساسيات تحليل الجمل الفعلية والاسمية البسيطة",
        "order": 1
    },
    {
        "id": 2,
        "name": "Level 2 - Complex Sentences",
        "arabic_name": "المستوى الثاني - الجمل المركبة", 
        "description": "Learn to analyze sentences with adjectives and prepositions",
        "arabic_description": "تعلم تحليل الجمل مع التوابع وحروف الجر",
        "order": 2
    }
]

CLEAN_LESSONS = [
    {
        "id": 1,
        "title": "Verbal Sentences - Past Tense",
        "arabic_title": "الجملة الفعلية - الفعل الماضي",
        "description": "Learn to analyze verbal sentences with past tense verbs, subjects, and direct objects",
        "arabic_description": "تعلم تحليل الجملة الفعلية مع الفعل الماضي والفاعل والمفعول به",
        "order": 1,
        "level_id": 1
    },
    {
        "id": 2,
        "title": "Verbal Sentences - Present Tense",
        "arabic_title": "الجملة الفعلية - الفعل المضارع",
        "description": "Learn to analyze verbal sentences with present tense verbs",
        "arabic_description": "تعلم تحليل الجملة الفعلية مع الفعل المضارع",
        "order": 2,
        "level_id": 1
    },
    {
        "id": 3,
        "title": "Nominal Sentences - Subject and Predicate",
        "arabic_title": "الجملة الاسمية - المبتدأ والخبر",
        "description": "Learn to analyze simple nominal sentences with subject and predicate",
        "arabic_description": "تعلم تحليل الجملة الاسمية البسيطة",
        "order": 3,
        "level_id": 1
    },
    {
        "id": 4,
        "title": "Sentences with Prepositions",
        "arabic_title": "الجملة الفعلية مع الجار والمجرور",
        "description": "Analyze sentences containing prepositions and prepositional phrases",
        "arabic_description": "تحليل الجمل التي تحتوي على حروف الجر",
        "order": 1,
        "level_id": 2
    },
    {
        "id": 5,
        "title": "Nominal Sentences with Adjectives",
        "arabic_title": "الجملة الاسمية مع النعت",
        "description": "Analyze sentences with adjectives and descriptive phrases",
        "arabic_description": "تحليل الجمل مع الصفات والنعوت",
        "order": 2,
        "level_id": 2
    }
]

COMPREHENSIVE_EXERCISES = [
    # Lesson 1: Past tense verbal sentences
    {
        "question": "Analyze the following sentence grammatically word by word",
        "question_arabic": "حلل الجملة التالية نحوياً كلمة كلمة",
        "exercise_type": "irab_analysis",
        "lesson_id": 1,
        "order": 1,
        "explanation": "A verbal sentence consisting of a past tense verb, subject, and direct object",
        "arabic_explanation": "جملة فعلية تتكون من فعل ماض وفاعل ومفعول به",
        "data": {
            "sentence": "ضرب عمرُ الكرةَ",
            "words": [
                {
                    "text": "ضرب",
                    "position": 0,
                    "questions": [
                        {
                            "question": "What type of word is 'ضرب'?",
                            "question_arabic": "ما نوع الكلمة 'ضرب'؟",
                            "options": ["Noun", "Verb", "Particle"],
                            "options_arabic": ["اسم", "فعل", "حرف"],
                            "correct_answer": "Verb",
                            "explanation": "'ضرب' is a past tense verb built on fatha",
                            "arabic_explanation": "ضرب فعل ماض مبني على الفتح"
                        },
                        {
                            "question": "What tense is the verb 'ضرب'?",
                            "question_arabic": "ما زمن الفعل 'ضرب'؟",
                            "options": ["Past", "Present", "Imperative"],
                            "options_arabic": ["ماض", "مضارع", "أمر"],
                            "correct_answer": "Past",
                            "explanation": "'ضرب' is a past tense verb indicating an action that occurred and ended",
                            "arabic_explanation": "ضرب فعل ماض يدل على حدث مضى وانقضى"
                        }
                    ]
                },
                {
                    "text": "عمرُ",
                    "position": 1,
                    "questions": [
                        {
                            "question": "What is the grammatical position of 'عمرُ'?",
                            "question_arabic": "ما موقع 'عمرُ' الإعرابي؟",
                            "options": ["Subject (فاعل)", "Direct Object (مفعول به)", "Predicate (مبتدأ)"],
                            "options_arabic": ["فاعل", "مفعول به", "مبتدأ"],
                            "correct_answer": "Subject (فاعل)",
                            "explanation": "'عمرُ' is the subject, nominative with visible damma",
                            "arabic_explanation": "عمرُ فاعل مرفوع وعلامة رفعه الضمة الظاهرة"
                        }
                    ]
                },
                {
                    "text": "الكرةَ",
                    "position": 2,
                    "questions": [
                        {
                            "question": "What is the grammatical position of 'الكرةَ'?",
                            "question_arabic": "ما موقع 'الكرةَ' الإعرابي؟",
                            "options": ["Subject (فاعل)", "Direct Object (مفعول به)", "Predicate (خبر)"],
                            "options_arabic": ["فاعل", "مفعول به", "خبر"],
                            "correct_answer": "Direct Object (مفعول به)",
                            "explanation": "'الكرةَ' is the direct object, accusative with visible fatha",
                            "arabic_explanation": "الكرةَ مفعول به منصوب وعلامة نصبه الفتحة الظاهرة"
                        }
                    ]
                }
            ]
        }
    },
    {
        "question": "Analyze the following sentence grammatically word by word",
        "question_arabic": "حلل الجملة التالية نحوياً كلمة كلمة",
        "exercise_type": "irab_analysis",
        "lesson_id": 1,
        "order": 2,
        "explanation": "A simple verbal sentence with a past tense verb",
        "arabic_explanation": "جملة فعلية بسيطة مع فعل ماض",
        "data": {
            "sentence": "قرأ أحمدُ الكتابَ",
            "words": [
                {
                    "text": "قرأ",
                    "position": 0,
                    "questions": [
                        {
                            "question": "What is the grammatical analysis of 'قرأ'?",
                            "question_arabic": "ما إعراب 'قرأ'؟",
                            "options": ["Built on fatha", "Nominative", "Accusative"],
                            "options_arabic": ["مبني على الفتح", "مرفوع", "منصوب"],
                            "correct_answer": "Built on fatha",
                            "explanation": "'قرأ' is a past tense verb built on fatha",
                            "arabic_explanation": "قرأ فعل ماض مبني على الفتح"
                        }
                    ]
                },
                {
                    "text": "أحمدُ",
                    "position": 1,
                    "questions": [
                        {
                            "question": "What is the grammatical analysis of 'أحمدُ'?",
                            "question_arabic": "ما إعراب 'أحمدُ'؟",
                            "options": ["Nominative subject", "Accusative object", "Nominative predicate"],
                            "options_arabic": ["فاعل مرفوع", "مفعول به منصوب", "مبتدأ مرفوع"],
                            "correct_answer": "Nominative subject",
                            "explanation": "'أحمدُ' is a nominative subject with damma marker",
                            "arabic_explanation": "أحمدُ فاعل مرفوع وعلامة رفعه الضمة"
                        }
                    ]
                },
                {
                    "text": "الكتابَ",
                    "position": 2,
                    "questions": [
                        {
                            "question": "What is the grammatical analysis of 'الكتابَ'?",
                            "question_arabic": "ما إعراب 'الكتابَ'؟",
                            "options": ["Nominative subject", "Accusative direct object", "Nominative predicate"],
                            "options_arabic": ["فاعل مرفوع", "مفعول به منصوب", "خبر مرفوع"],
                            "correct_answer": "Accusative direct object",
                            "explanation": "'الكتابَ' is accusative direct object with fatha marker",
                            "arabic_explanation": "الكتابَ مفعول به منصوب وعلامة نصبه الفتحة"
                        }
                    ]
                }
            ]
        }
    },
    {
        "question": "Analyze the following sentence grammatically word by word",
        "question_arabic": "حلل الجملة التالية نحوياً كلمة كلمة",
        "exercise_type": "irab_analysis", 
        "lesson_id": 1,
        "order": 3,
        "explanation": "A verbal sentence with past tense verb, subject and direct object",
        "arabic_explanation": "جملة فعلية مع فعل ماض وفاعل ومفعول به",
        "data": {
            "sentence": "كتب الطالبُ الواجبَ",
            "words": [
                {
                    "text": "كتب",
                    "position": 0,
                    "questions": [
                        {
                            "question": "What type is 'كتب'?",
                            "question_arabic": "ما نوع 'كتب'؟",
                            "options": ["Past verb", "Present verb", "Noun"],
                            "options_arabic": ["فعل ماض", "فعل مضارع", "اسم"],
                            "correct_answer": "Past verb",
                            "explanation": "'كتب' is a past tense verb built on fatha",
                            "arabic_explanation": "كتب فعل ماض مبني على الفتح"
                        }
                    ]
                },
                {
                    "text": "الطالبُ",
                    "position": 1,
                    "questions": [
                        {
                            "question": "Why is 'الطالبُ' nominative?",
                            "question_arabic": "لماذا 'الطالبُ' مرفوع؟",
                            "options": ["Because it's the subject", "Because it's the predicate", "Because it's the object"],
                            "options_arabic": ["لأنه فاعل", "لأنه مبتدأ", "لأنه خبر"],
                            "correct_answer": "Because it's the subject",
                            "explanation": "'الطالبُ' is the subject and subjects are always nominative",
                            "arabic_explanation": "الطالبُ فاعل والفاعل مرفوع دائماً"
                        }
                    ]
                },
                {
                    "text": "الواجبَ",
                    "position": 2,
                    "questions": [
                        {
                            "question": "Why is 'الواجبَ' accusative?",
                            "question_arabic": "لماذا 'الواجبَ' منصوب؟",
                            "options": ["Because it's a direct object", "Because it's a subject", "Because it's a genitive"],
                            "options_arabic": ["لأنه مفعول به", "لأنه فاعل", "لأنه مضاف إليه"],
                            "correct_answer": "Because it's a direct object",
                            "explanation": "'الواجبَ' is a direct object and direct objects are always accusative",
                            "arabic_explanation": "الواجبَ مفعول به والمفعول به منصوب دائماً"
                        }
                    ]
                }
            ]
        }
    },
    
    # Lesson 2: Present tense verbal sentences  
    {
        "question": "Analyze the following sentence grammatically word by word",
        "question_arabic": "حلل الجملة التالية نحوياً كلمة كلمة",
        "exercise_type": "irab_analysis",
        "lesson_id": 2,
        "order": 1,
        "explanation": "A verbal sentence with a present tense verb",
        "arabic_explanation": "جملة فعلية مع فعل مضارع",
        "data": {
            "sentence": "يدرس محمدٌ النحوَ",
            "words": [
                {
                    "text": "يدرس",
                    "position": 0,
                    "questions": [
                        {
                            "question": "What tense is 'يدرس'?",
                            "question_arabic": "ما زمن 'يدرس'؟",
                            "options": ["Past", "Present", "Imperative"],
                            "options_arabic": ["ماض", "مضارع", "أمر"],
                            "correct_answer": "Present",
                            "explanation": "'يدرس' is a present tense verb, nominative with damma",
                            "arabic_explanation": "يدرس فعل مضارع مرفوع وعلامة رفعه الضمة"
                        },
                        {
                            "question": "What is the grammatical case of 'يدرس'?",
                            "question_arabic": "ما إعراب 'يدرس'؟",
                            "options": ["Nominative", "Accusative", "Jussive"],
                            "options_arabic": ["مرفوع", "منصوب", "مجزوم"],
                            "correct_answer": "Nominative",
                            "explanation": "Present tense verbs are nominative when not preceded by a particle",
                            "arabic_explanation": "الفعل المضارع مرفوع إذا لم يسبق بناصب أو جازم"
                        }
                    ]
                },
                {
                    "text": "محمدٌ",
                    "position": 1,
                    "questions": [
                        {
                            "question": "What is the position of 'محمدٌ'?",
                            "question_arabic": "ما موقع 'محمدٌ'؟",
                            "options": ["Subject", "Direct object", "Predicate"],
                            "options_arabic": ["فاعل", "مفعول به", "مبتدأ"],
                            "correct_answer": "Subject",
                            "explanation": "'محمدٌ' is the subject, nominative with damma",
                            "arabic_explanation": "محمدٌ فاعل مرفوع وعلامة رفعه الضمة"
                        }
                    ]
                },
                {
                    "text": "النحوَ",
                    "position": 2,
                    "questions": [
                        {
                            "question": "What is the position of 'النحوَ'?",
                            "question_arabic": "ما موقع 'النحوَ'؟",
                            "options": ["Subject", "Direct object", "Predicate"],
                            "options_arabic": ["فاعل", "مفعول به", "خبر"],
                            "correct_answer": "Direct object",
                            "explanation": "'النحوَ' is the direct object, accusative with fatha",
                            "arabic_explanation": "النحوَ مفعول به منصوب وعلامة نصبه الفتحة"
                        }
                    ]
                }
            ]
        }
    },
    
    # Lesson 3: Nominal sentences
    {
        "question": "Analyze the following sentence grammatically word by word",
        "question_arabic": "حلل الجملة التالية نحوياً كلمة كلمة",
        "exercise_type": "irab_analysis",
        "lesson_id": 3,
        "order": 1,
        "explanation": "A simple nominal sentence with subject and predicate",
        "arabic_explanation": "جملة اسمية بسيطة من مبتدأ وخبر",
        "data": {
            "sentence": "الطالبُ مجتهدٌ",
            "words": [
                {
                    "text": "الطالبُ",
                    "position": 0,
                    "questions": [
                        {
                            "question": "What is the grammatical position of 'الطالبُ'?",
                            "question_arabic": "ما موقع 'الطالبُ' الإعرابي؟",
                            "options": ["Subject (مبتدأ)", "Predicate (خبر)", "Agent (فاعل)"],
                            "options_arabic": ["مبتدأ", "خبر", "فاعل"],
                            "correct_answer": "Subject (مبتدأ)",
                            "explanation": "'الطالبُ' is the subject, nominative with damma",
                            "arabic_explanation": "الطالبُ مبتدأ مرفوع وعلامة رفعه الضمة"
                        },
                        {
                            "question": "Why is 'الطالبُ' nominative?",
                            "question_arabic": "لماذا 'الطالبُ' مرفوع؟",
                            "options": ["Because it's a subject", "Because it's an agent", "Because it's an object"],
                            "options_arabic": ["لأنه مبتدأ", "لأنه فاعل", "لأنه مفعول به"],
                            "correct_answer": "Because it's a subject",
                            "explanation": "Subjects are always nominative",
                            "arabic_explanation": "المبتدأ مرفوع دائماً"
                        }
                    ]
                },
                {
                    "text": "مجتهدٌ",
                    "position": 1,
                    "questions": [
                        {
                            "question": "What is the grammatical position of 'مجتهدٌ'?",
                            "question_arabic": "ما موقع 'مجتهدٌ' الإعرابي؟",
                            "options": ["Predicate", "Subject", "Agent"],
                            "options_arabic": ["خبر", "مبتدأ", "فاعل"],
                            "correct_answer": "Predicate",
                            "explanation": "'مجتهدٌ' is the predicate of the subject, nominative with damma",
                            "arabic_explanation": "مجتهدٌ خبر المبتدأ مرفوع وعلامة رفعه الضمة"
                        }
                    ]
                }
            ]
        }
    }
]

async def clear_database():
    """Clear all existing lessons and exercises"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        await db.execute("DELETE FROM exercises")
        await db.execute("DELETE FROM lessons")
        await db.execute("DELETE FROM levels")
        await db.commit()
        print("Cleared all existing levels, lessons and exercises")

async def add_clean_levels():
    """Add the focused grammar levels"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        for level in CLEAN_LEVELS:
            await db.execute(
                """INSERT OR REPLACE INTO levels (id, name, arabic_name, description, arabic_description, "order") 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (level["id"], level["name"], level["arabic_name"], 
                 level["description"], level["arabic_description"], level["order"])
            )
        await db.commit()
        print(f"Added {len(CLEAN_LEVELS)} focused grammar levels")

async def add_clean_lessons():
    """Add the focused grammar lessons"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        for lesson in CLEAN_LESSONS:
            await db.execute(
                """INSERT OR REPLACE INTO lessons (id, title, arabic_title, description, arabic_description, "order", level_id) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (lesson["id"], lesson["title"], lesson["arabic_title"], 
                 lesson["description"], lesson["arabic_description"], lesson["order"], lesson["level_id"])
            )
        await db.commit()
        print(f"Added {len(CLEAN_LESSONS)} focused grammar lessons")

async def add_comprehensive_exercises():
    """Add comprehensive exercises to the database"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        for exercise_data in COMPREHENSIVE_EXERCISES:
            # Convert the data structure to JSON for storage
            correct_answer_json = json.dumps(exercise_data["data"], ensure_ascii=False)
            
            # Insert the exercise
            cursor = await db.execute(
                """INSERT INTO exercises 
                   (question, question_arabic, exercise_type, correct_answer, explanation, arabic_explanation, "order", lesson_id) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    exercise_data["question"],
                    exercise_data["question_arabic"],
                    exercise_data["exercise_type"],
                    correct_answer_json,
                    exercise_data["explanation"],
                    exercise_data["arabic_explanation"],
                    exercise_data["order"],
                    exercise_data["lesson_id"]
                )
            )
            
            exercise_id = cursor.lastrowid
            print(f"Added exercise: {exercise_data['question']} (Lesson {exercise_data['lesson_id']})")
        
        await db.commit()
        print(f"Successfully added {len(COMPREHENSIVE_EXERCISES)} comprehensive exercises!")

async def show_curriculum_summary():
    """Show the new curriculum summary"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        db.row_factory = aiosqlite.Row
        
        # Show levels
        cursor = await db.execute("SELECT * FROM levels ORDER BY \"order\"")
        levels = await cursor.fetchall()
        
        print(f"\n=== CLEAN ENGLISH-PRIMARY IRAB CURRICULUM ===")
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
    """Main function to set up clean irab curriculum"""
    print("Setting up clean English-primary irab analysis curriculum...")
    print("=" * 60)
    
    await clear_database()
    await add_clean_levels()
    await add_clean_lessons()
    await add_comprehensive_exercises()
    await show_curriculum_summary()
    
    print("\n✅ Clean English-primary irab curriculum setup complete!")

if __name__ == "__main__":
    asyncio.run(main())
