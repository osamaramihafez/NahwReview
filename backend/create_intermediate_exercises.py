import asyncio
import aiosqlite

async def create_intermediate_exercises():
    """Create comprehensive exercises for intermediate grammar sections"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        
        # Lesson 6: Past Tense Verbs (الفعل الماضي)
        exercises_lesson_6 = [
            {
                "question": "Identify the past tense verb in: كَتَبَ الطَّالِبُ الدَّرْسَ",
                "question_arabic": "عيّن الفعل الماضي في: كَتَبَ الطَّالِبُ الدَّرْسَ",
                "exercise_type": "multiple_choice",
                "correct_answer": "كَتَبَ",
                "explanation": "كَتَبَ is the past tense verb meaning 'wrote'. Past tense verbs are identified by their form and the fact that they describe completed actions.",
                "order": 1,
                "lesson_id": 6,
                "options": [
                    {"option_text": "كَتَبَ", "is_correct": True},
                    {"option_text": "الطَّالِبُ", "is_correct": False},
                    {"option_text": "الدَّرْسَ", "is_correct": False},
                    {"option_text": "None of the above", "is_correct": False}
                ]
            },
            {
                "question": "What is the root of the verb ذَهَبَ (went)?",
                "question_arabic": "ما جذر الفعل ذَهَبَ؟",
                "exercise_type": "multiple_choice",
                "correct_answer": "ذ ه ب",
                "explanation": "The root of ذَهَبَ is ذ-ه-ب. Arabic verbs are built on three-letter roots that carry the basic meaning.",
                "order": 2,
                "lesson_id": 6,
                "options": [
                    {"option_text": "ذ ه ب", "is_correct": True},
                    {"option_text": "ذ ب ه", "is_correct": False},
                    {"option_text": "ه ذ ب", "is_correct": False},
                    {"option_text": "ب ه ذ", "is_correct": False}
                ]
            },
            {
                "question": "Fill in the blank: أَكَلَ الوَلَدُ _____ (the apple)",
                "question_arabic": "أكمل الفراغ: أَكَلَ الوَلَدُ _____",
                "exercise_type": "fill_blank",
                "correct_answer": "التُّفَّاحَةَ",
                "explanation": "التُّفَّاحَةَ (the apple) is in the accusative case (منصوب) because it's the direct object of the verb أَكَلَ.",
                "order": 3,
                "lesson_id": 6
            },
            {
                "question": "Which sentence contains a past tense verb?",
                "question_arabic": "أي جملة تحتوي على فعل ماض؟",
                "exercise_type": "multiple_choice",
                "correct_answer": "قَرَأَ المُعَلِّمُ الكِتَابَ",
                "explanation": "قَرَأَ is a past tense verb meaning 'read'. The other options contain present tense verbs or no verbs at all.",
                "order": 4,
                "lesson_id": 6,
                "options": [
                    {"option_text": "قَرَأَ المُعَلِّمُ الكِتَابَ", "is_correct": True},
                    {"option_text": "يَقْرَأُ المُعَلِّمُ الكِتَابَ", "is_correct": False},
                    {"option_text": "المُعَلِّمُ مُجْتَهِدٌ", "is_correct": False},
                    {"option_text": "في المَدْرَسَةِ", "is_correct": False}
                ]
            },
            {
                "question": "What does the past tense verb لَعِبَ mean in English?",
                "question_arabic": "ما معنى الفعل الماضي لَعِبَ؟",
                "exercise_type": "multiple_choice",
                "correct_answer": "played",
                "explanation": "لَعِبَ means 'played' or 'he played'. This is a common past tense verb form.",
                "order": 5,
                "lesson_id": 6,
                "options": [
                    {"option_text": "played", "is_correct": True},
                    {"option_text": "studies", "is_correct": False},
                    {"option_text": "wrote", "is_correct": False},
                    {"option_text": "went", "is_correct": False}
                ]
            }
        ]
        
        # Lesson 7: Present/Future Tense (الفعل المضارع)
        exercises_lesson_7 = [
            {
                "question": "Identify the present tense verb in: يَكْتُبُ الطَّالِبُ الوَاجِبَ",
                "question_arabic": "عيّن الفعل المضارع في: يَكْتُبُ الطَّالِبُ الوَاجِبَ",
                "exercise_type": "multiple_choice",
                "correct_answer": "يَكْتُبُ",
                "explanation": "يَكْتُبُ is the present tense verb meaning 'writes/is writing'. Present tense verbs start with one of the letters أ، ت، ي، ن.",
                "order": 1,
                "lesson_id": 7,
                "options": [
                    {"option_text": "يَكْتُبُ", "is_correct": True},
                    {"option_text": "الطَّالِبُ", "is_correct": False},
                    {"option_text": "الوَاجِبَ", "is_correct": False},
                    {"option_text": "None of the above", "is_correct": False}
                ]
            },
            {
                "question": "What are the prefix letters for present tense verbs?",
                "question_arabic": "ما هي حروف المضارعة؟",
                "exercise_type": "multiple_choice",
                "correct_answer": "أ، ت، ي، ن",
                "explanation": "The prefix letters for present tense verbs are أ، ت، ي، ن (collected in the word أَنْتِي or نَأْتِي).",
                "order": 2,
                "lesson_id": 7,
                "options": [
                    {"option_text": "أ، ت، ي، ن", "is_correct": True},
                    {"option_text": "ب، ت، ث، ج", "is_correct": False},
                    {"option_text": "ك، ل، م، و", "is_correct": False},
                    {"option_text": "س، ش، ص، ض", "is_correct": False}
                ]
            },
            {
                "question": "Convert to present tense: كَتَبَ (he wrote)",
                "question_arabic": "حوّل إلى المضارع: كَتَبَ",
                "exercise_type": "fill_blank",
                "correct_answer": "يَكْتُبُ",
                "explanation": "The present tense of كَتَبَ is يَكْتُبُ (he writes/is writing). The prefix ي indicates third person masculine singular.",
                "order": 3,
                "lesson_id": 7
            },
            {
                "question": "Which verb means 'I study' in Arabic?",
                "question_arabic": "أي فعل يعني 'أدرس' بالعربية؟",
                "exercise_type": "multiple_choice",
                "correct_answer": "أَدْرُسُ",
                "explanation": "أَدْرُسُ means 'I study'. The prefix أ indicates first person singular in present tense verbs.",
                "order": 4,
                "lesson_id": 7,
                "options": [
                    {"option_text": "أَدْرُسُ", "is_correct": True},
                    {"option_text": "تَدْرُسُ", "is_correct": False},
                    {"option_text": "يَدْرُسُ", "is_correct": False},
                    {"option_text": "دَرَسَ", "is_correct": False}
                ]
            },
            {
                "question": "What is the difference between يَلْعَبُ and تَلْعَبُ?",
                "question_arabic": "ما الفرق بين يَلْعَبُ و تَلْعَبُ؟",
                "exercise_type": "multiple_choice",
                "correct_answer": "يَلْعَبُ (he plays), تَلْعَبُ (she/you play)",
                "explanation": "يَلْعَبُ means 'he plays' (third person masculine), while تَلْعَبُ can mean 'she plays' or 'you play' depending on context.",
                "order": 5,
                "lesson_id": 7,
                "options": [
                    {"option_text": "يَلْعَبُ (he plays), تَلْعَبُ (she/you play)", "is_correct": True},
                    {"option_text": "Both mean the same thing", "is_correct": False},
                    {"option_text": "يَلْعَبُ (past), تَلْعَبُ (present)", "is_correct": False},
                    {"option_text": "Different verbs entirely", "is_correct": False}
                ]
            }
        ]
        
        # Lesson 8: Subject and Predicate (المبتدأ والخبر)
        exercises_lesson_8 = [
            {
                "question": "In the sentence 'الطَّالِبُ مُجْتَهِدٌ', identify the subject (المبتدأ)",
                "question_arabic": "في الجملة 'الطَّالِبُ مُجْتَهِدٌ'، عيّن المبتدأ",
                "exercise_type": "multiple_choice",
                "correct_answer": "الطَّالِبُ",
                "explanation": "الطَّالِبُ is the subject (المبتدأ). The subject is the noun that the sentence is talking about, always in the nominative case.",
                "order": 1,
                "lesson_id": 8,
                "options": [
                    {"option_text": "الطَّالِبُ", "is_correct": True},
                    {"option_text": "مُجْتَهِدٌ", "is_correct": False},
                    {"option_text": "Both words", "is_correct": False},
                    {"option_text": "Neither word", "is_correct": False}
                ]
            },
            {
                "question": "In the sentence 'الكِتَابُ جَدِيدٌ', identify the predicate (الخبر)",
                "question_arabic": "في الجملة 'الكِتَابُ جَدِيدٌ'، عيّن الخبر",
                "exercise_type": "multiple_choice",
                "correct_answer": "جَدِيدٌ",
                "explanation": "جَدِيدٌ is the predicate (الخبر). The predicate tells us something about the subject, always in the nominative case.",
                "order": 2,
                "lesson_id": 8,
                "options": [
                    {"option_text": "جَدِيدٌ", "is_correct": True},
                    {"option_text": "الكِتَابُ", "is_correct": False},
                    {"option_text": "Both words", "is_correct": False},
                    {"option_text": "Neither word", "is_correct": False}
                ]
            },
            {
                "question": "Complete the nominal sentence: المُعَلِّمُ _____",
                "question_arabic": "أكمل الجملة الاسمية: المُعَلِّمُ _____",
                "exercise_type": "fill_blank",
                "correct_answer": "مُتَمَيِّزٌ",
                "explanation": "المُعَلِّمُ مُتَمَيِّزٌ (The teacher is excellent). The predicate must be in the nominative case with damma ending.",
                "order": 3,
                "lesson_id": 8
            },
            {
                "question": "What case are both المبتدأ and الخبر always in?",
                "question_arabic": "في أي حالة إعرابية يكون المبتدأ والخبر دائماً؟",
                "exercise_type": "multiple_choice",
                "correct_answer": "Nominative (مرفوع)",
                "explanation": "Both المبتدأ (subject) and الخبر (predicate) are always in the nominative case (مرفوع), typically marked with damma.",
                "order": 4,
                "lesson_id": 8,
                "options": [
                    {"option_text": "Nominative (مرفوع)", "is_correct": True},
                    {"option_text": "Accusative (منصوب)", "is_correct": False},
                    {"option_text": "Genitive (مجرور)", "is_correct": False},
                    {"option_text": "Different cases", "is_correct": False}
                ]
            },
            {
                "question": "Which sentence is a proper nominal sentence?",
                "question_arabic": "أي جملة هي جملة اسمية صحيحة؟",
                "exercise_type": "multiple_choice",
                "correct_answer": "البَيْتُ كَبِيرٌ",
                "explanation": "البَيْتُ كَبِيرٌ is a proper nominal sentence with subject (البَيْتُ) and predicate (كَبِيرٌ) both in nominative case.",
                "order": 5,
                "lesson_id": 8,
                "options": [
                    {"option_text": "البَيْتُ كَبِيرٌ", "is_correct": True},
                    {"option_text": "ذَهَبَ الوَلَدُ", "is_correct": False},
                    {"option_text": "في المَدْرَسَةِ", "is_correct": False},
                    {"option_text": "يَكْتُبُ الطَّالِبُ", "is_correct": False}
                ]
            }
        ]
        
        # Lesson 9: Subject/Doer (الفاعل)
        exercises_lesson_9 = [
            {
                "question": "In 'كَتَبَ الطَّالِبُ الرِّسَالَةَ', identify the doer (الفاعل)",
                "question_arabic": "في 'كَتَبَ الطَّالِبُ الرِّسَالَةَ'، عيّن الفاعل",
                "exercise_type": "multiple_choice",
                "correct_answer": "الطَّالِبُ",
                "explanation": "الطَّالِبُ is the doer (الفاعل). The doer is the one who performs the action of the verb, always in nominative case.",
                "order": 1,
                "lesson_id": 9,
                "options": [
                    {"option_text": "الطَّالِبُ", "is_correct": True},
                    {"option_text": "كَتَبَ", "is_correct": False},
                    {"option_text": "الرِّسَالَةَ", "is_correct": False},
                    {"option_text": "None of the above", "is_correct": False}
                ]
            },
            {
                "question": "What case is the فاعل (doer) always in?",
                "question_arabic": "في أي حالة إعرابية يكون الفاعل دائماً؟",
                "exercise_type": "multiple_choice",
                "correct_answer": "Nominative (مرفوع)",
                "explanation": "The فاعل (doer) is always in the nominative case (مرفوع), typically marked with damma.",
                "order": 2,
                "lesson_id": 9,
                "options": [
                    {"option_text": "Nominative (مرفوع)", "is_correct": True},
                    {"option_text": "Accusative (منصوب)", "is_correct": False},
                    {"option_text": "Genitive (مجرور)", "is_correct": False},
                    {"option_text": "Varies by context", "is_correct": False}
                ]
            },
            {
                "question": "Complete the sentence with the correct doer: لَعِبَ _____ في الحَدِيقَةِ",
                "question_arabic": "أكمل الجملة بالفاعل الصحيح: لَعِبَ _____ في الحَدِيقَةِ",
                "exercise_type": "fill_blank",
                "correct_answer": "الأَطْفَالُ",
                "explanation": "الأَطْفَالُ (the children) is correct. The doer must be in nominative case with damma ending.",
                "order": 3,
                "lesson_id": 9
            },
            {
                "question": "In 'جَاءَ الضَّيْفُ', what is the grammatical term for الضَّيْفُ?",
                "question_arabic": "في 'جَاءَ الضَّيْفُ'، ما المصطلح النحوي لـ الضَّيْفُ؟",
                "exercise_type": "multiple_choice",
                "correct_answer": "فاعل (doer)",
                "explanation": "الضَّيْفُ is the فاعل (doer) because it's the one performing the action of coming (جَاءَ).",
                "order": 4,
                "lesson_id": 9,
                "options": [
                    {"option_text": "فاعل (doer)", "is_correct": True},
                    {"option_text": "مفعول به (direct object)", "is_correct": False},
                    {"option_text": "مبتدأ (subject)", "is_correct": False},
                    {"option_text": "خبر (predicate)", "is_correct": False}
                ]
            },
            {
                "question": "Which sentence has a hidden pronoun as the doer?",
                "question_arabic": "أي جملة فيها ضمير مستتر كفاعل؟",
                "exercise_type": "multiple_choice",
                "correct_answer": "ذَهَبَ إلى المَسْجِدِ",
                "explanation": "In 'ذَهَبَ إلى المَسْجِدِ', the doer is a hidden pronoun (هو) within the verb ذَهَبَ.",
                "order": 5,
                "lesson_id": 9,
                "options": [
                    {"option_text": "ذَهَبَ إلى المَسْجِدِ", "is_correct": True},
                    {"option_text": "ذَهَبَ الرَّجُلُ إلى المَسْجِدِ", "is_correct": False},
                    {"option_text": "الرَّجُلُ في المَسْجِدِ", "is_correct": False},
                    {"option_text": "يَذْهَبُ الرَّجُلُ", "is_correct": False}
                ]
            }
        ]
        
        # Lesson 10: Direct Object (المفعول به)
        exercises_lesson_10 = [
            {
                "question": "In 'أَكَلَ الوَلَدُ التُّفَّاحَةَ', identify the direct object (المفعول به)",
                "question_arabic": "في 'أَكَلَ الوَلَدُ التُّفَّاحَةَ'، عيّن المفعول به",
                "exercise_type": "multiple_choice",
                "correct_answer": "التُّفَّاحَةَ",
                "explanation": "التُّفَّاحَةَ is the direct object (المفعول به). It's what receives the action of the verb, always in accusative case.",
                "order": 1,
                "lesson_id": 10,
                "options": [
                    {"option_text": "التُّفَّاحَةَ", "is_correct": True},
                    {"option_text": "الوَلَدُ", "is_correct": False},
                    {"option_text": "أَكَلَ", "is_correct": False},
                    {"option_text": "None of the above", "is_correct": False}
                ]
            },
            {
                "question": "What case is the مفعول به (direct object) always in?",
                "question_arabic": "في أي حالة إعرابية يكون المفعول به دائماً؟",
                "exercise_type": "multiple_choice",
                "correct_answer": "Accusative (منصوب)",
                "explanation": "The مفعول به (direct object) is always in the accusative case (منصوب), typically marked with fatha.",
                "order": 2,
                "lesson_id": 10,
                "options": [
                    {"option_text": "Accusative (منصوب)", "is_correct": True},
                    {"option_text": "Nominative (مرفوع)", "is_correct": False},
                    {"option_text": "Genitive (مجرور)", "is_correct": False},
                    {"option_text": "Varies by context", "is_correct": False}
                ]
            },
            {
                "question": "Complete with the correct direct object: قَرَأَ الطَّالِبُ _____",
                "question_arabic": "أكمل بالمفعول به الصحيح: قَرَأَ الطَّالِبُ _____",
                "exercise_type": "fill_blank",
                "correct_answer": "الكِتَابَ",
                "explanation": "الكِتَابَ (the book) is correct. The direct object must be in accusative case with fatha ending.",
                "order": 3,
                "lesson_id": 10
            },
            {
                "question": "Which sentence contains a direct object?",
                "question_arabic": "أي جملة تحتوي على مفعول به؟",
                "exercise_type": "multiple_choice",
                "correct_answer": "شَرِبَ الرَّجُلُ الماءَ",
                "explanation": "In 'شَرِبَ الرَّجُلُ الماءَ', الماءَ is the direct object. The other sentences are either nominal or don't have direct objects.",
                "order": 4,
                "lesson_id": 10,
                "options": [
                    {"option_text": "شَرِبَ الرَّجُلُ الماءَ", "is_correct": True},
                    {"option_text": "الرَّجُلُ طَوِيلٌ", "is_correct": False},
                    {"option_text": "ذَهَبَ إلى البَيْتِ", "is_correct": False},
                    {"option_text": "في الحَدِيقَةِ أَشْجَارٌ", "is_correct": False}
                ]
            },
            {
                "question": "What is the difference between الفاعل and المفعول به?",
                "question_arabic": "ما الفرق بين الفاعل والمفعول به؟",
                "exercise_type": "multiple_choice",
                "correct_answer": "الفاعل does the action (مرفوع), المفعول به receives it (منصوب)",
                "explanation": "الفاعل is the doer of the action (nominative case), while المفعول به is what receives the action (accusative case).",
                "order": 5,
                "lesson_id": 10,
                "options": [
                    {"option_text": "الفاعل does the action (مرفوع), المفعول به receives it (منصوب)", "is_correct": True},
                    {"option_text": "They are the same thing", "is_correct": False},
                    {"option_text": "الفاعل is definite, المفعول به is indefinite", "is_correct": False},
                    {"option_text": "No difference in meaning", "is_correct": False}
                ]
            }
        ]
        
        # Insert all exercises
        all_exercises = [
            *exercises_lesson_6,
            *exercises_lesson_7, 
            *exercises_lesson_8,
            *exercises_lesson_9,
            *exercises_lesson_10
        ]
        
        for exercise in all_exercises:
            # Insert exercise
            cursor = await db.execute(
                "INSERT INTO exercises (question, question_arabic, exercise_type, correct_answer, explanation, \"order\", lesson_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (exercise["question"], exercise["question_arabic"], exercise["exercise_type"], 
                 exercise["correct_answer"], exercise["explanation"], exercise["order"], exercise["lesson_id"])
            )
            exercise_id = cursor.lastrowid
            
            # Insert options if it's multiple choice
            if exercise["exercise_type"] == "multiple_choice" and "options" in exercise:
                for option in exercise["options"]:
                    await db.execute(
                        "INSERT INTO exercise_options (option_text, is_correct, exercise_id) VALUES (?, ?, ?)",
                        (option["option_text"], option["is_correct"], exercise_id)
                    )
        
        await db.commit()
        print(f"Successfully created {len(all_exercises)} exercises for intermediate grammar!")
        
        # Show summary
        print("\n=== EXERCISE SUMMARY ===")
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
                count = await cursor.fetchone()
                print(f"Lesson {lesson_id} - {lesson_names[lesson_id]}: {count['count']} exercises")

if __name__ == "__main__":
    asyncio.run(create_intermediate_exercises())
