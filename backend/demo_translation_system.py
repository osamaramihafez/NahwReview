import asyncio
import aiosqlite

async def demonstrate_translation_system():
    """Demonstrate the translation system with sample exercises"""
    
    async with aiosqlite.connect("nahw_exercises.db") as db:
        
        print("🎯 TRANSLATION SYSTEM DEMONSTRATION")
        print("=" * 50)
        
        # First, let's see what translation keys we have
        print("\n📚 Available Translation Keys:")
        cursor = await db.execute("""
            SELECT tk.key_name, tk.category, 
                   GROUP_CONCAT(t.language_code || ':' || t.text, ' | ') as translations
            FROM translation_keys tk
            LEFT JOIN translations t ON tk.id = t.translation_key_id
            GROUP BY tk.id, tk.key_name, tk.category
            ORDER BY tk.category, tk.key_name
        """)
        keys = await cursor.fetchall()
        
        current_category = None
        for key_name, category, translations in keys:
            if category != current_category:
                print(f"\n📖 {category or 'Other'}:")
                current_category = category
            print(f"  • {key_name}: {translations}")
        
        # Now let's create a sample exercise using the translation system
        print(f"\n🔧 Creating Sample Exercise Using Translation Keys")
        print("-" * 50)
        
        # Create a sample exercise
        exercise_data = {
            "question": "What type of word is 'كَتَبَ'?",
            "question_arabic": "ما نوع الكلمة 'كَتَبَ'؟",
            "exercise_type": "multiple_choice",
            "correct_answer": "فعل",
            "explanation": "كَتَبَ is a past tense verb meaning 'wrote'",
            "order": 1,
            "lesson_id": 1
        }
        
        # Create the exercise
        cursor = await db.execute("""
            INSERT INTO exercises 
            (question, question_arabic, exercise_type, correct_answer, explanation, "order", lesson_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            exercise_data["question"],
            exercise_data["question_arabic"], 
            exercise_data["exercise_type"],
            exercise_data["correct_answer"],
            exercise_data["explanation"],
            exercise_data["order"],
            exercise_data["lesson_id"]
        ))
        
        exercise_id = cursor.lastrowid
        print(f"✅ Created exercise with ID: {exercise_id}")
        
        # Now add options using translation keys
        options_with_translation_keys = [
            {"key": "verb", "is_correct": True},
            {"key": "noun", "is_correct": False},
            {"key": "particle", "is_correct": False}
        ]
        
        for option in options_with_translation_keys:
            # Get the translation key ID
            cursor = await db.execute(
                "SELECT id FROM translation_keys WHERE key_name = ?", 
                (option["key"],)
            )
            key_row = await cursor.fetchone()
            
            if key_row:
                key_id = key_row[0]
                await db.execute("""
                    INSERT INTO exercise_options_v2 
                    (translation_key_id, is_correct, exercise_id) 
                    VALUES (?, ?, ?)
                """, (key_id, option["is_correct"], exercise_id))
                print(f"✅ Added option using translation key: {option['key']}")
            else:
                print(f"❌ Translation key not found: {option['key']}")
        
        await db.commit()
        
        # Now demonstrate localization
        print(f"\n🌍 LOCALIZATION DEMONSTRATION")
        print("-" * 35)
        
        # Function to get localized options
        async def get_localized_options(exercise_id, language_code):
            cursor = await db.execute("""
                SELECT 
                    eo.is_correct,
                    CASE 
                        WHEN eo.translation_key_id IS NOT NULL THEN 
                            COALESCE(t.text, tk.key_name)
                        ELSE 
                            eo.option_text 
                    END as option_text
                FROM exercise_options_v2 eo
                LEFT JOIN translation_keys tk ON eo.translation_key_id = tk.id
                LEFT JOIN translations t ON tk.id = t.translation_key_id 
                                          AND t.language_code = ? 
                                          AND t.is_primary = 1
                WHERE eo.exercise_id = ?
                ORDER BY eo.id
            """, (language_code, exercise_id))
            return await cursor.fetchall()
        
        # Show options in Arabic
        print("\n🔤 Options in Arabic:")
        arabic_options = await get_localized_options(exercise_id, "ar")
        for is_correct, option_text in arabic_options:
            print(f"  {'✓' if is_correct else '✗'} {option_text}")
        
        # Show options in English
        print("\n🔤 Options in English:")
        english_options = await get_localized_options(exercise_id, "en")
        for is_correct, option_text in english_options:
            print(f"  {'✓' if is_correct else '✗'} {option_text}")
        
        # Create another example with mixed translation keys and direct text
        print(f"\n🔧 Creating Exercise with Mixed Options")
        print("-" * 45)
        
        # Create another exercise
        exercise_data_2 = {
            "question": "What is the grammatical case of the subject in 'كَتَبَ الطَّالِبُ'?",
            "question_arabic": "ما حالة إعراب الفاعل في 'كَتَبَ الطَّالِبُ'؟",
            "exercise_type": "multiple_choice",
            "correct_answer": "مرفوع",
            "explanation": "The subject (فاعل) is always in the nominative case",
            "order": 2,
            "lesson_id": 1
        }
        
        cursor = await db.execute("""
            INSERT INTO exercises 
            (question, question_arabic, exercise_type, correct_answer, explanation, "order", lesson_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            exercise_data_2["question"],
            exercise_data_2["question_arabic"], 
            exercise_data_2["exercise_type"],
            exercise_data_2["correct_answer"],
            exercise_data_2["explanation"],
            exercise_data_2["order"],
            exercise_data_2["lesson_id"]
        ))
        
        exercise_id_2 = cursor.lastrowid
        print(f"✅ Created exercise with ID: {exercise_id_2}")
        
        # Add options: some with translation keys, some with direct text
        mixed_options = [
            {"translation_key": "nominative", "is_correct": True},
            {"translation_key": "accusative", "is_correct": False},
            {"text": "مجهول", "is_correct": False},  # Direct text option
        ]
        
        for option in mixed_options:
            if "translation_key" in option:
                # Use translation key
                cursor = await db.execute(
                    "SELECT id FROM translation_keys WHERE key_name = ?", 
                    (option["translation_key"],)
                )
                key_row = await cursor.fetchone()
                
                if key_row:
                    key_id = key_row[0]
                    await db.execute("""
                        INSERT INTO exercise_options_v2 
                        (translation_key_id, is_correct, exercise_id) 
                        VALUES (?, ?, ?)
                    """, (key_id, option["is_correct"], exercise_id_2))
                    print(f"✅ Added option using translation key: {option['translation_key']}")
            else:
                # Use direct text
                await db.execute("""
                    INSERT INTO exercise_options_v2 
                    (option_text, is_correct, exercise_id) 
                    VALUES (?, ?, ?)
                """, (option["text"], option["is_correct"], exercise_id_2))
                print(f"✅ Added option using direct text: {option['text']}")
        
        await db.commit()
        
        # Show the mixed options
        print(f"\n🌍 Mixed Options Example (Arabic):")
        mixed_arabic_options = await get_localized_options(exercise_id_2, "ar")
        for is_correct, option_text in mixed_arabic_options:
            print(f"  {'✓' if is_correct else '✗'} {option_text}")
        
        print(f"\n🌍 Mixed Options Example (English):")
        mixed_english_options = await get_localized_options(exercise_id_2, "en")
        for is_correct, option_text in mixed_english_options:
            print(f"  {'✓' if is_correct else '✗'} {option_text}")
        
        # Show summary of benefits
        print(f"\n🎉 TRANSLATION SYSTEM BENEFITS")
        print("-" * 35)
        print("✅ Consistent terminology across exercises")
        print("✅ Easy language switching")
        print("✅ Centralized translation management")
        print("✅ Support for mixed content (keys + direct text)")
        print("✅ Easy to add new languages")
        print("✅ Reduced duplicate data")
        
        # Show next steps
        print(f"\n📋 NEXT STEPS FOR IMPLEMENTATION")
        print("-" * 40)
        print("1. Update your API endpoints to accept language parameter")
        print("2. Modify frontend to request options in user's preferred language")
        print("3. Create admin interface for managing translations")
        print("4. Add new grammatical terms as needed")
        print("5. Consider adding more languages (French, Spanish, etc.)")

if __name__ == "__main__":
    asyncio.run(demonstrate_translation_system())
