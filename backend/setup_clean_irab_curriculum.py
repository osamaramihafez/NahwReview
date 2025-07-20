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
                            "correct_answer_arabic": "فعل",
                            "explanation": "'ضرب' is a verb",
                            "arabic_explanation": "ضرب فعل"
                        },
                        {
                            "question": "What tense is the verb 'ضرب'?",
                            "question_arabic": "ما زمن الفعل 'ضرب'؟",
                            "options": ["Past", "Present", "Imperative", "Future", "Conditional", "Subjunctive"],
                            "options_arabic": ["ماض", "مضارع", "أمر", "مستقبل", "شرطي", "منصوب"],
                            "correct_answer": "Past",
                            "correct_answer_arabic": "ماض",
                            "explanation": "'ضرب' is a past tense verb",
                            "arabic_explanation": "ضرب فعل ماض"
                        },
                        {
                            "question": "What is the grammatical construction of 'ضرب'?",
                            "question_arabic": "ما إعراب 'ضرب' من ناحية البناء؟",
                            "options": ["Built", "Declined", "Indeclinable"],
                            "options_arabic": ["مبني", "معرب", "غير منصرف"],
                            "correct_answer": "Built",
                            "correct_answer_arabic": "مبني",
                            "explanation": "Past tense verbs are always built (مبني), not declined",
                            "arabic_explanation": "الأفعال الماضية مبنية دائماً وليست معربة"
                        },
                        {
                            "question": "What is 'ضرب' built on?",
                            "question_arabic": "على ماذا بني 'ضرب'؟",
                            "options": ["Fatha", "Damma", "Sukun", "Kasra", "Joined to pronoun", "Joined to nun of emphasis"],
                            "options_arabic": ["الفتح", "الضم", "السكون", "الكسر", "اتصل بضمير", "اتصل بنون التوكيد"],
                            "correct_answer": "Fatha",
                            "correct_answer_arabic": "الفتح",
                            "explanation": "'ضرب' is built on fatha because it's a sound past tense verb",
                            "arabic_explanation": "ضرب مبني على الفتح لأنه فعل ماض صحيح"
                        },
                        {
                            "question": "Give the complete irab of 'ضرب'",
                            "question_arabic": "أعرب 'ضرب' إعراباً كاملاً",
                            "options": [
                                "فعل ماض مبني على الفتح",
                                "فعل مضارع مرفوع بالضمة",
                                "اسم مرفوع بالضمة"
                            ],
                            "options_arabic": [
                                "فعل ماض مبني على الفتح",
                                "فعل مضارع مرفوع بالضمة", 
                                "اسم مرفوع بالضمة"
                            ],
                            "correct_answer": "فعل ماض مبني على الفتح",
                            "correct_answer_arabic": "فعل ماض مبني على الفتح",
                            "explanation": "Complete irab: 'ضرب' is a past tense verb built on fatha",
                            "arabic_explanation": "الإعراب الكامل: ضرب فعل ماض مبني على الفتح"
                        }
                    ]
                },
                {
                    "text": "عمرُ",
                    "position": 1,
                    "questions": [
                        {
                            "question": "What type of word is 'عمرُ'?",
                            "question_arabic": "ما نوع الكلمة 'عمرُ'؟",
                            "options": ["Noun", "Verb", "Particle"],
                            "options_arabic": ["اسم", "فعل", "حرف"],
                            "correct_answer": "Noun",
                            "correct_answer_arabic": "اسم",
                            "explanation": "'عمرُ' is a proper noun",
                            "arabic_explanation": "عمرُ اسم علم"
                        },
                        {
                            "question": "What is the grammatical position of 'عمرُ'?",
                            "question_arabic": "ما موقع 'عمرُ' الإعرابي؟",
                            "options": ["Subject", "Direct Object", "Predicate of مبتدأ", "Subject of nominal sentence", "Prepositional object", "Indirect object"],
                            "options_arabic": ["فاعل", "مفعول به", "خبر", "مبتدأ", "مجرور", "مفعول له"],
                            "correct_answer": "Subject",
                            "correct_answer_arabic": "فاعل",
                            "explanation": "'عمرُ' is the subject (doer) of the verb 'ضرب'",
                            "arabic_explanation": "عمرُ فاعل للفعل 'ضرب'"
                        },
                        {
                            "question": "What is the case of 'عمرُ'?",
                            "question_arabic": "ما حالة 'عمرُ' الإعرابية؟",
                            "options": ["Nominative", "Accusative", "Genitive"],
                            "options_arabic": ["مرفوع", "منصوب", "مجرور"],
                            "correct_answer": "Nominative",
                            "correct_answer_arabic": "مرفوع",
                            "explanation": "'عمرُ' is nominative because it's the subject",
                            "arabic_explanation": "عمرُ مرفوع لأنه فاعل"
                        },
                        {
                            "question": "What is the case marker of 'عمرُ'?",
                            "question_arabic": "ما علامة إعراب 'عمرُ'؟",
                            "options": ["Visible damma", "Estimated damma", "Alif", "Waw", "Visible fatha", "Visible kasra"],
                            "options_arabic": ["الضمة الظاهرة", "الضمة المقدرة", "الألف", "الواو", "الفتحة الظاهرة", "الكسرة الظاهرة"],
                            "correct_answer": "Visible damma",
                            "correct_answer_arabic": "الضمة الظاهرة",
                            "explanation": "'عمرُ' has a visible damma as the case marker",
                            "arabic_explanation": "عمرُ علامة إعرابه الضمة الظاهرة"
                        },
                        {
                            "question": "Why is 'عمرُ' nominative?",
                            "question_arabic": "لماذا 'عمرُ' مرفوع؟",
                            "options": ["Because it's the subject", "Because it's the object", "Because it's after a preposition", "Because it's a predicate", "Because it's an adjective", "Because it's in construct state"],
                            "options_arabic": ["لأنه فاعل", "لأنه مفعول به", "لأنه مجرور بحرف الجر", "لأنه خبر", "لأنه نعت", "لأنه مضاف إليه"],
                            "correct_answer": "Because it's the subject",
                            "correct_answer_arabic": "لأنه فاعل",
                            "explanation": "Subjects are always nominative in Arabic",
                            "arabic_explanation": "الفاعل مرفوع دائماً في اللغة العربية"
                        },
                        {
                            "question": "Give the complete irab of 'عمرُ'",
                            "question_arabic": "أعرب 'عمرُ' إعراباً كاملاً",
                            "options": [
                                "فاعل مرفوع وعلامة رفعه الضمة الظاهرة",
                                "مفعول به منصوب وعلامة نصبه الفتحة",
                                "مبتدأ مرفوع وعلامة رفعه الضمة"
                            ],
                            "options_arabic": [
                                "فاعل مرفوع وعلامة رفعه الضمة الظاهرة",
                                "مفعول به منصوب وعلامة نصبه الفتحة",
                                "مبتدأ مرفوع وعلامة رفعه الضمة"
                            ],
                            "correct_answer": "فاعل مرفوع وعلامة رفعه الضمة الظاهرة",
                            "correct_answer_arabic": "فاعل مرفوع وعلامة رفعه الضمة الظاهرة",
                            "explanation": "Complete irab: 'عمرُ' is a nominative subject with visible damma marker",
                            "arabic_explanation": "الإعراب الكامل: عمرُ فاعل مرفوع وعلامة رفعه الضمة الظاهرة"
                        }
                    ]
                },
                {
                    "text": "الكرةَ",
                    "position": 2,
                    "questions": [
                        {
                            "question": "What type of word is 'الكرةَ'?",
                            "question_arabic": "ما نوع الكلمة 'الكرةَ'؟",
                            "options": ["Noun", "Verb", "Particle"],
                            "options_arabic": ["اسم", "فعل", "حرف"],
                            "correct_answer": "Noun",
                            "correct_answer_arabic": "اسم",
                            "explanation": "'الكرةَ' is a definite noun with the definite article 'ال'",
                            "arabic_explanation": "الكرةَ اسم معرف بأل التعريف"
                        },
                        {
                            "question": "What is the grammatical position of 'الكرةَ'?",
                            "question_arabic": "ما موقع 'الكرةَ' الإعرابي؟",
                            "options": ["Subject (فاعل)", "Direct Object (مفعول به)", "Predicate (خبر)", "Subject of nominal sentence (مبتدأ)", "Prepositional object (مجرور)", "Circumstantial object (مفعول فيه)", "Absolute object (مفعول مطلق)"],
                            "options_arabic": ["فاعل", "مفعول به", "خبر", "مبتدأ", "مجرور", "مفعول فيه", "مفعول مطلق"],
                            "correct_answer": "Direct Object (مفعول به)",
                            "correct_answer_arabic": "مفعول به",
                            "explanation": "'الكرةَ' is the direct object of the verb 'ضرب'",
                            "arabic_explanation": "الكرةَ مفعول به للفعل 'ضرب'"
                        },
                        {
                            "question": "What is the case of 'الكرةَ'?",
                            "question_arabic": "ما حالة 'الكرةَ' الإعرابية؟",
                            "options": ["Nominative (مرفوع)", "Accusative (منصوب)", "Genitive (مجرور)"],
                            "options_arabic": ["مرفوع", "منصوب", "مجرور"],
                            "correct_answer": "Accusative (منصوب)",
                            "correct_answer_arabic": "منصوب",
                            "explanation": "'الكرةَ' is accusative because it's the direct object",
                            "arabic_explanation": "الكرةَ منصوب لأنه مفعول به"
                        },
                        {
                            "question": "What is the case marker of 'الكرةَ'?",
                            "question_arabic": "ما علامة إعراب 'الكرةَ'؟",
                            "options": ["Visible fatha (الفتحة الظاهرة)", "Estimated fatha (الفتحة المقدرة)", "Alif (الألف)", "Ya (الياء)", "Visible kasra (الكسرة الظاهرة)", "Visible damma (الضمة الظاهرة)"],
                            "options_arabic": ["الفتحة الظاهرة", "الفتحة المقدرة", "الألف", "الياء", "الكسرة الظاهرة", "الضمة الظاهرة"],
                            "correct_answer": "Visible fatha (الفتحة الظاهرة)",
                            "correct_answer_arabic": "الفتحة الظاهرة",
                            "explanation": "'الكرةَ' has a visible fatha as the case marker",
                            "arabic_explanation": "الكرةَ علامة إعرابه الفتحة الظاهرة"
                        },
                        {
                            "question": "Why is 'الكرةَ' accusative?",
                            "question_arabic": "لماذا 'الكرةَ' منصوب؟",
                            "options": ["Because it's a direct object", "Because it's a subject", "Because it's after a preposition", "Because it's a predicate", "Because it's an adjective following accusative noun", "Because it's a circumstantial object", "Because it's an absolute object"],
                            "options_arabic": ["لأنه مفعول به", "لأنه فاعل", "لأنه مجرور بحرف الجر", "لأنه خبر", "لأنه نعت لمنصوب", "لأنه مفعول فيه", "لأنه مفعول مطلق"],
                            "correct_answer": "Because it's a direct object",
                            "correct_answer_arabic": "لأنه مفعول به",
                            "explanation": "Direct objects are always accusative in Arabic",
                            "arabic_explanation": "المفعول به منصوب دائماً في اللغة العربية"
                        },
                        {
                            "question": "Give the complete irab of 'الكرةَ'",
                            "question_arabic": "أعرب 'الكرةَ' إعراباً كاملاً",
                            "options": [
                                "مفعول به منصوب وعلامة نصبه الفتحة الظاهرة",
                                "فاعل مرفوع وعلامة رفعه الضمة",
                                "مجرور بحرف الجر وعلامة جره الكسرة"
                            ],
                            "options_arabic": [
                                "مفعول به منصوب وعلامة نصبه الفتحة الظاهرة",
                                "فاعل مرفوع وعلامة رفعه الضمة",
                                "مجرور بحرف الجر وعلامة جره الكسرة"
                            ],
                            "correct_answer": "مفعول به منصوب وعلامة نصبه الفتحة الظاهرة",
                            "correct_answer_arabic": "مفعول به منصوب وعلامة نصبه الفتحة الظاهرة",
                            "explanation": "Complete irab: 'الكرةَ' is an accusative direct object with visible fatha marker",
                            "arabic_explanation": "الإعراب الكامل: الكرةَ مفعول به منصوب وعلامة نصبه الفتحة الظاهرة"
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
                            "question": "What type of word is 'قرأ'?",
                            "question_arabic": "ما نوع الكلمة 'قرأ'؟",
                            "options": ["Noun", "Verb", "Particle"],
                            "options_arabic": ["اسم", "فعل", "حرف"],
                            "correct_answer": "Verb",
                            "correct_answer_arabic": "فعل",
                            "explanation": "'قرأ' is a verb",
                            "arabic_explanation": "قرأ فعل"
                        },
                        {
                            "question": "What tense is 'قرأ'?",
                            "question_arabic": "ما زمن 'قرأ'؟",
                            "options": ["Past", "Present", "Imperative"],
                            "options_arabic": ["ماض", "مضارع", "أمر"],
                            "correct_answer": "Past",
                            "correct_answer_arabic": "ماض",
                            "explanation": "'قرأ' is a past tense verb",
                            "arabic_explanation": "قرأ فعل ماض"
                        },
                        {
                            "question": "What is the construction type of 'قرأ'?",
                            "question_arabic": "ما نوع إعراب 'قرأ'؟",
                            "options": ["Built (مبني)", "Declined (معرب)", "Indeclinable (غير منصرف)"],
                            "options_arabic": ["مبني", "معرب", "غير منصرف"],
                            "correct_answer": "Built",
                            "correct_answer_arabic": "مبني",
                            "explanation": "Past tense verbs are always built",
                            "arabic_explanation": "الأفعال الماضية مبنية دائماً"
                        },
                        {
                            "question": "What is 'قرأ' built on?",
                            "question_arabic": "على ماذا بني 'قرأ'؟",
                            "options": ["Fatha (الفتح)", "Damma (الضم)", "Sukun (السكون)", "Kasra (الكسر)", "Joined to pronoun", "Joined to nun of emphasis"],
                            "options_arabic": ["الفتح", "الضم", "السكون", "الكسر", "اتصل بضمير", "اتصل بنون التوكيد"],
                            "correct_answer": "Fatha (الفتح)",
                            "correct_answer_arabic": "الفتح",
                            "explanation": "'قرأ' is built on fatha",
                            "arabic_explanation": "قرأ مبني على الفتح"
                        },
                        {
                            "question": "Give the complete irab of 'قرأ'",
                            "question_arabic": "أعرب 'قرأ' إعراباً كاملاً",
                            "options": [
                                "فعل ماض مبني على الفتح",
                                "فعل مضارع مرفوع بالضمة",
                                "اسم مرفوع بالضمة"
                            ],
                            "options_arabic": [
                                "فعل ماض مبني على الفتح",
                                "فعل مضارع مرفوع بالضمة",
                                "اسم مرفوع بالضمة"
                            ],
                            "correct_answer": "فعل ماض مبني على الفتح",
                            "correct_answer_arabic": "فعل ماض مبني على الفتح",
                            "explanation": "Complete irab: 'قرأ' is a past tense verb built on fatha",
                            "arabic_explanation": "الإعراب الكامل: قرأ فعل ماض مبني على الفتح"
                        }
                    ]
                },
                {
                    "text": "أحمدُ",
                    "position": 1,
                    "questions": [
                        {
                            "question": "What type of word is 'أحمدُ'?",
                            "question_arabic": "ما نوع الكلمة 'أحمدُ'؟",
                            "options": ["Noun", "Verb", "Particle"],
                            "options_arabic": ["اسم", "فعل", "حرف"],
                            "correct_answer": "Noun",
                            "correct_answer_arabic": "اسم",
                            "explanation": "'أحمدُ' is a proper noun",
                            "arabic_explanation": "أحمدُ اسم علم"
                        },
                        {
                            "question": "What is the grammatical position of 'أحمدُ'?",
                            "question_arabic": "ما موقع 'أحمدُ' الإعرابي؟",
                            "options": ["Subject (فاعل)", "Direct Object (مفعول به)", "Predicate of مبتدأ (خبر)", "Subject of nominal sentence (مبتدأ)", "Prepositional object (مجرور)", "Indirect object (مفعول له)"],
                            "options_arabic": ["فاعل", "مفعول به", "خبر", "مبتدأ", "مجرور", "مفعول له"],
                            "correct_answer": "Subject",
                            "correct_answer_arabic": "فاعل",
                            "explanation": "'أحمدُ' is the subject of the verb 'قرأ'",
                            "arabic_explanation": "أحمدُ فاعل للفعل 'قرأ'"
                        },
                        {
                            "question": "What is the case of 'أحمدُ'?",
                            "question_arabic": "ما حالة 'أحمدُ' الإعرابية؟",
                            "options": ["Nominative (مرفوع)", "Accusative (منصوب)", "Genitive (مجرور)"],
                            "options_arabic": ["مرفوع", "منصوب", "مجرور"],
                            "correct_answer": "Nominative",
                            "correct_answer_arabic": "مرفوع",
                            "explanation": "'أحمدُ' is nominative because it's the subject",
                            "arabic_explanation": "أحمدُ مرفوع لأنه فاعل"
                        },
                        {
                            "question": "What is the case marker of 'أحمدُ'?",
                            "question_arabic": "ما علامة إعراب 'أحمدُ'؟",
                            "options": ["Visible damma (الضمة الظاهرة)", "Estimated damma (الضمة المقدرة)", "Alif (الألف)", "Waw (الواو)", "Visible fatha (الفتحة الظاهرة)", "Visible kasra (الكسرة الظاهرة)"],
                            "options_arabic": ["الضمة الظاهرة", "الضمة المقدرة", "الألف", "الواو", "الفتحة الظاهرة", "الكسرة الظاهرة"],
                            "correct_answer": "Visible damma",
                            "correct_answer_arabic": "الضمة الظاهرة",
                            "explanation": "'أحمدُ' has a visible damma",
                            "arabic_explanation": "أحمدُ علامة إعرابه الضمة الظاهرة"
                        },
                        {
                            "question": "Give the complete irab of 'أحمدُ'",
                            "question_arabic": "أعرب 'أحمدُ' إعراباً كاملاً",
                            "options": [
                                "فاعل مرفوع وعلامة رفعه الضمة الظاهرة",
                                "مفعول به منصوب وعلامة نصبه الفتحة",
                                "مبتدأ مرفوع وعلامة رفعه الضمة"
                            ],
                            "options_arabic": [
                                "فاعل مرفوع وعلامة رفعه الضمة الظاهرة",
                                "مفعول به منصوب وعلامة نصبه الفتحة",
                                "مبتدأ مرفوع وعلامة رفعه الضمة"
                            ],
                            "correct_answer": "فاعل مرفوع وعلامة رفعه الضمة الظاهرة",
                            "correct_answer_arabic": "فاعل مرفوع وعلامة رفعه الضمة الظاهرة",
                            "explanation": "Complete irab: 'أحمدُ' is a nominative subject with visible damma",
                            "arabic_explanation": "الإعراب الكامل: أحمدُ فاعل مرفوع وعلامة رفعه الضمة الظاهرة"
                        }
                    ]
                },
                {
                    "text": "الكتابَ",
                    "position": 2,
                    "questions": [
                        {
                            "question": "What type of word is 'الكتابَ'?",
                            "question_arabic": "ما نوع الكلمة 'الكتابَ'؟",
                            "options": ["Noun", "Verb", "Particle"],
                            "options_arabic": ["اسم", "فعل", "حرف"],
                            "correct_answer": "Noun",
                            "correct_answer_arabic": "اسم",
                            "explanation": "'الكتابَ' is a definite noun",
                            "arabic_explanation": "الكتابَ اسم معرف بأل"
                        },
                        {
                            "question": "What is the grammatical position of 'الكتابَ'?",
                            "question_arabic": "ما موقع 'الكتابَ' الإعرابي؟",
                            "options": ["Subject (فاعل)", "Direct Object (مفعول به)", "Predicate (خبر)", "Subject of nominal sentence (مبتدأ)", "Prepositional object (مجرور)", "Circumstantial object (مفعول فيه)", "Absolute object (مفعول مطلق)"],
                            "options_arabic": ["فاعل", "مفعول به", "خبر", "مبتدأ", "مجرور", "مفعول فيه", "مفعول مطلق"],
                            "correct_answer": "Direct Object (مفعول به)",
                            "correct_answer_arabic": "مفعول به",
                            "explanation": "'الكتابَ' is the direct object of 'قرأ'",
                            "arabic_explanation": "الكتابَ مفعول به للفعل 'قرأ'"
                        },
                        {
                            "question": "What is the case of 'الكتابَ'?",
                            "question_arabic": "ما حالة 'الكتابَ' الإعرابية؟",
                            "options": ["Nominative (مرفوع)", "Accusative (منصوب)", "Genitive (مجرور)"],
                            "options_arabic": ["مرفوع", "منصوب", "مجرور"],
                            "correct_answer": "Accusative (منصوب)",
                            "correct_answer_arabic": "منصوب",
                            "explanation": "'الكتابَ' is accusative because it's a direct object",
                            "arabic_explanation": "الكتابَ منصوب لأنه مفعول به"
                        },
                        {
                            "question": "What is the case marker of 'الكتابَ'?",
                            "question_arabic": "ما علامة إعراب 'الكتابَ'؟",
                            "options": ["Visible fatha (الفتحة الظاهرة)", "Estimated fatha (الفتحة المقدرة)", "Alif (الألف)", "Ya (الياء)", "Visible kasra (الكسرة الظاهرة)", "Visible damma (الضمة الظاهرة)"],
                            "options_arabic": ["الفتحة الظاهرة", "الفتحة المقدرة", "الألف", "الياء", "الكسرة الظاهرة", "الضمة الظاهرة"],
                            "correct_answer": "Visible fatha (الفتحة الظاهرة)",
                            "correct_answer_arabic": "الفتحة الظاهرة",
                            "explanation": "'الكتابَ' has a visible fatha",
                            "arabic_explanation": "الكتابَ علامة إعرابه الفتحة الظاهرة"
                        },
                        {
                            "question": "Give the complete irab of 'الكتابَ'",
                            "question_arabic": "أعرب 'الكتابَ' إعراباً كاملاً",
                            "options": [
                                "مفعول به منصوب وعلامة نصبه الفتحة الظاهرة",
                                "فاعل مرفوع وعلامة رفعه الضمة",
                                "مجرور بحرف الجر وعلامة جره الكسرة"
                            ],
                            "options_arabic": [
                                "مفعول به منصوب وعلامة نصبه الفتحة الظاهرة",
                                "فاعل مرفوع وعلامة رفعه الضمة",
                                "مجرور بحرف الجر وعلامة جره الكسرة"
                            ],
                            "correct_answer": "مفعول به منصوب وعلامة نصبه الفتحة الظاهرة",
                            "correct_answer_arabic": "مفعول به منصوب وعلامة نصبه الفتحة الظاهرة",
                            "explanation": "Complete irab: 'الكتابَ' is an accusative direct object with visible fatha",
                            "arabic_explanation": "الإعراب الكامل: الكتابَ مفعول به منصوب وعلامة نصبه الفتحة الظاهرة"
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
                            "correct_answer_arabic": "فعل ماض",
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
                            "correct_answer_arabic": "لأنه فاعل",
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
                            "correct_answer_arabic": "لأنه مفعول به",
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
                            "options": ["Past", "Present", "Imperative", "Future", "Conditional", "Subjunctive"],
                            "options_arabic": ["ماض", "مضارع", "أمر", "مستقبل", "شرطي", "منصوب"],
                            "correct_answer": "Present",
                            "correct_answer_arabic": "مضارع",
                            "explanation": "'يدرس' is a present tense verb, nominative with damma",
                            "arabic_explanation": "يدرس فعل مضارع مرفوع وعلامة رفعه الضمة"
                        },
                        {
                            "question": "What is the grammatical case of 'يدرس'?",
                            "question_arabic": "ما إعراب 'يدرس'؟",
                            "options": ["Nominative", "Accusative", "Jussive", "Built", "Conditional", "Subjunctive"],
                            "options_arabic": ["مرفوع", "منصوب", "مجزوم", "مبني", "شرطي", "منصوب بأن"],
                            "correct_answer": "Nominative",
                            "correct_answer_arabic": "مرفوع",
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
                            "correct_answer_arabic": "فاعل",
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
                            "correct_answer_arabic": "مفعول به",
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
                            "options": ["Subject (مبتدأ)", "Predicate (خبر)", "Agent (فاعل)", "Direct Object (مفعول به)", "Prepositional object (مجرور)", "Adjective (نعت)"],
                            "options_arabic": ["مبتدأ", "خبر", "فاعل", "مفعول به", "مجرور", "نعت"],
                            "correct_answer": "Subject (مبتدأ)",
                            "correct_answer_arabic": "مبتدأ",
                            "explanation": "'الطالبُ' is the subject, nominative with damma",
                            "arabic_explanation": "الطالبُ مبتدأ مرفوع وعلامة رفعه الضمة"
                        },
                        {
                            "question": "Why is 'الطالبُ' nominative?",
                            "question_arabic": "لماذا 'الطالبُ' مرفوع؟",
                            "options": ["Because it's a subject", "Because it's an agent", "Because it's an object", "Because it's a predicate", "Because it's an adjective", "Because it's after a preposition"],
                            "options_arabic": ["لأنه مبتدأ", "لأنه فاعل", "لأنه مفعول به", "لأنه خبر", "لأنه نعت", "لأنه مجرور بحرف الجر"],
                            "correct_answer": "Because it's a subject",
                            "correct_answer_arabic": "لأنه مبتدأ",
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
                            "options": ["Predicate", "Subject", "Agent", "Direct Object", "Adjective", "Prepositional object"],
                            "options_arabic": ["خبر", "مبتدأ", "فاعل", "مفعول به", "نعت", "مجرور"],
                            "correct_answer": "Predicate",
                            "correct_answer_arabic": "خبر",
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
