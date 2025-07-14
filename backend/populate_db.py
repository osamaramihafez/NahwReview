import asyncio
import aiosqlite
from database import init_database

async def populate_database():
    # Initialize database tables
    await init_database()
    
    async with aiosqlite.connect("nahw_exercises.db") as db:
        try:
            # Create levels
            levels_data = [
                ("Beginner Foundations", "Basic concepts of Arabic grammar and declension", 1),
                ("Intermediate Grammar", "Verbs, particles, and grammatical roles", 2),
                ("Advanced Syntax", "Advanced nouns, verbs, and complex structures", 3),
                ("Mastery & Nuances", "Specialized grammar and stylistic structures", 4)
            ]
            
            level_ids = []
            for name, description, order in levels_data:
                cursor = await db.execute(
                    "INSERT INTO levels (name, description, \"order\") VALUES (?, ?, ?)",
                    (name, description, order)
                )
                level_ids.append(cursor.lastrowid)
            
            await db.commit()
            
            # Level 1 Lessons
            level1_lessons = [
                ("Definition of Nahw", "تعريف النحو", "Understanding what Arabic grammar (Nahw) is and its importance", 1, level_ids[0]),
                ("Word and Speech", "الكلمة والكلام", "Basic building blocks of Arabic language", 2, level_ids[0]),
                ("Parts of Speech", "أقسام الكلمة", "Noun, Verb, and Particle identification", 3, level_ids[0]),
                ("Nominal and Verbal Sentences", "الجملة الاسمية والجملة الفعلية", "Understanding sentence types in Arabic", 4, level_ids[0]),
                ("Grammatical Vowel Marks", "الحركات الإعرابية", "Damma, Fatha, Kasra, and Sukoon", 5, level_ids[0])
            ]
            
            # Level 2 Lessons
            level2_lessons = [
                ("Past Tense Verbs", "الفعل الماضي", "Understanding and using past tense verbs", 1, level_ids[1]),
                ("Present/Future Tense", "الفعل المضارع", "Present and future tense verb forms", 2, level_ids[1]),
                ("Subject and Predicate", "المبتدأ والخبر", "Understanding the main components of nominal sentences", 3, level_ids[1]),
                ("Subject/Doer", "الفاعل", "Identifying and using the grammatical subject", 4, level_ids[1]),
                ("Direct Object", "المفعول به", "Understanding direct objects in Arabic sentences", 5, level_ids[1])
            ]
            
            all_lessons = level1_lessons + level2_lessons
            lesson_ids = []
            
            for title, arabic_title, description, order, level_id in all_lessons:
                cursor = await db.execute(
                    "INSERT INTO lessons (title, arabic_title, description, \"order\", level_id) VALUES (?, ?, ?, ?, ?)",
                    (title, arabic_title, description, order, level_id)
                )
                lesson_ids.append(cursor.lastrowid)
            
            await db.commit()
            
            # Sample exercises for the first lesson
            exercises_data = [
                (
                    "What does 'النحو' (Nahw) mean?",
                    "ما معنى النحو؟",
                    "multiple_choice",
                    "Arabic grammar",
                    "النحو (Nahw) is the science of Arabic grammar that studies the relationships between words in sentences.",
                    lesson_ids[0]
                ),
                (
                    "Which of the following is NOT a part of speech in Arabic?",
                    "أي من التالي ليس من أقسام الكلمة؟",
                    "multiple_choice",
                    "Adjective",
                    "Arabic has three main parts of speech: اسم (noun), فعل (verb), and حرف (particle). Adjectives are considered a type of noun.",
                    lesson_ids[2]
                ),
                (
                    "Complete the sentence: الطالب _____ الكتاب",
                    "أكمل الجملة: الطالب _____ الكتاب",
                    "multiple_choice",
                    "يقرأ",
                    "يقرأ (reads) is the correct present tense verb form that agrees with الطالب (the student).",
                    lesson_ids[5] if len(lesson_ids) > 5 else lesson_ids[1]
                )
            ]
            
            exercise_ids = []
            for question, question_arabic, exercise_type, correct_answer, explanation, lesson_id in exercises_data:
                cursor = await db.execute(
                    "INSERT INTO exercises (question, question_arabic, exercise_type, correct_answer, explanation, lesson_id) VALUES (?, ?, ?, ?, ?, ?)",
                    (question, question_arabic, exercise_type, correct_answer, explanation, lesson_id)
                )
                exercise_ids.append(cursor.lastrowid)
            
            await db.commit()
            
            # Add options for multiple choice questions
            options_data = [
                # Options for first exercise
                ("Arabic grammar", True, exercise_ids[0]),
                ("Arabic poetry", False, exercise_ids[0]),
                ("Arabic literature", False, exercise_ids[0]),
                ("Arabic morphology", False, exercise_ids[0]),
                
                # Options for second exercise
                ("Noun", False, exercise_ids[1]),
                ("Verb", False, exercise_ids[1]),
                ("Particle", False, exercise_ids[1]),
                ("Adjective", True, exercise_ids[1]),
            ]
            
            for option_text, is_correct, exercise_id in options_data:
                await db.execute(
                    "INSERT INTO exercise_options (option_text, is_correct, exercise_id) VALUES (?, ?, ?)",
                    (option_text, is_correct, exercise_id)
                )
            
            await db.commit()
            
            print("Database populated successfully!")
            
        except Exception as e:
            print(f"Error populating database: {e}")
            await db.rollback()

async def main():
    await populate_database()

if __name__ == "__main__":
    asyncio.run(main())
