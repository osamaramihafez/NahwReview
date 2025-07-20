# Translation System Integration for crud.py
# Add these functions to your existing crud.py file

async def get_translation_key_id(db: aiosqlite.Connection, key_name: str) -> Optional[int]:
    """Get translation key ID by key name"""
    async with db.execute(
        "SELECT id FROM translation_keys WHERE key_name = ?", 
        (key_name,)
    ) as cursor:
        row = await cursor.fetchone()
        return row[0] if row else None

async def get_translation(db: aiosqlite.Connection, key_name: str, language_code: str = "ar") -> str:
    """Get translation for a key in specified language"""
    async with db.execute("""
        SELECT t.text 
        FROM translations t
        JOIN translation_keys tk ON t.translation_key_id = tk.id
        WHERE tk.key_name = ? AND t.language_code = ? AND t.is_primary = 1
    """, (key_name, language_code)) as cursor:
        row = await cursor.fetchone()
        return row[0] if row else key_name

async def get_exercise_options_localized(db: aiosqlite.Connection, 
                                       exercise_id: int, 
                                       language_code: str = "ar") -> List[Dict]:
    """Get exercise options with proper localization"""
    
    async with db.execute("""
        SELECT 
            eo.id,
            eo.is_correct,
            CASE 
                WHEN eo.translation_key_id IS NOT NULL THEN 
                    COALESCE(t.text, tk.key_name)
                ELSE 
                    eo.option_text 
            END as option_text,
            tk.key_name as translation_key
        FROM exercise_options eo
        LEFT JOIN translation_keys tk ON eo.translation_key_id = tk.id
        LEFT JOIN translations t ON tk.id = t.translation_key_id 
                                  AND t.language_code = ? 
                                  AND t.is_primary = 1
        WHERE eo.exercise_id = ?
        ORDER BY eo.id
    """, (language_code, exercise_id)) as cursor:
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def create_exercise_with_translated_options(db: aiosqlite.Connection,
                                                exercise_data: dict,
                                                options_data: List[Dict]) -> int:
    """Create exercise with options that use translation keys where possible"""
    
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
        exercise_data.get("order", 0),
        exercise_data["lesson_id"]
    ))
    
    exercise_id = cursor.lastrowid
    
    # Add options
    for option in options_data:
        if "translation_key" in option:
            # Use translation key
            key_id = await get_translation_key_id(db, option["translation_key"])
            if key_id:
                await db.execute("""
                    INSERT INTO exercise_options 
                    (translation_key_id, is_correct, exercise_id) 
                    VALUES (?, ?, ?)
                """, (key_id, option["is_correct"], exercise_id))
            else:
                print(f"Warning: Translation key '{option['translation_key']}' not found")
                # Fallback to direct text if translation key is not found
                await db.execute("""
                    INSERT INTO exercise_options 
                    (option_text, is_correct, exercise_id) 
                    VALUES (?, ?, ?)
                """, (option.get("option_text", option["translation_key"]), option["is_correct"], exercise_id))
        else:
            # Fallback to direct text
            await db.execute("""
                INSERT INTO exercise_options 
                (option_text, is_correct, exercise_id) 
                VALUES (?, ?, ?)
            """, (option["option_text"], option["is_correct"], exercise_id))
    
    await db.commit()
    return exercise_id

# Update the existing get_exercise_by_id function to support localization
async def get_exercise_by_id_localized(db: aiosqlite.Connection, 
                                     exercise_id: int, 
                                     language_code: str = "ar") -> Optional[Dict[str, Any]]:
    """Get exercise by ID with localized options"""
    async with db.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,)) as cursor:
        row = await cursor.fetchone()
        if row:
            exercise = dict(row)
            exercise['options'] = await get_exercise_options_localized(db, exercise_id, language_code)
            return exercise
        return None

async def get_exercises_by_lesson_localized(db: aiosqlite.Connection, 
                                          lesson_id: int,
                                          language_code: str = "ar") -> List[Dict[str, Any]]:
    """Get all exercises for a lesson with localized options"""
    async with db.execute("SELECT * FROM exercises WHERE lesson_id = ? ORDER BY \"order\"", (lesson_id,)) as cursor:
        rows = await cursor.fetchall()
        exercises = []
        for row in rows:
            exercise = dict(row)
            exercise['options'] = await get_exercise_options_localized(db, exercise['id'], language_code)
            exercises.append(exercise)
        return exercises

# Admin functions for translation management
async def get_all_translation_keys_with_stats(db: aiosqlite.Connection) -> List[Dict]:
    """Get all translation keys with usage statistics"""
    async with db.execute("""
        SELECT 
            tk.id,
            tk.key_name,
            tk.category,
            tk.description,
            COUNT(DISTINCT t.language_code) as language_count,
            COUNT(DISTINCT eo.exercise_id) as usage_count,
            GROUP_CONCAT(DISTINCT t.language_code) as available_languages
        FROM translation_keys tk
        LEFT JOIN translations t ON tk.id = t.translation_key_id
        LEFT JOIN exercise_options eo ON tk.id = eo.translation_key_id
        GROUP BY tk.id, tk.key_name, tk.category, tk.description
        ORDER BY usage_count DESC
    """) as cursor:
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def get_missing_translations(db: aiosqlite.Connection, language_code: str) -> List[Dict]:
    """Find translation keys missing translations for a specific language"""
    async with db.execute("""
        SELECT tk.key_name, tk.category, tk.description
        FROM translation_keys tk
        WHERE tk.id NOT IN (
            SELECT DISTINCT translation_key_id 
            FROM translations 
            WHERE language_code = ?
        )
        ORDER BY tk.category, tk.key_name
    """, (language_code,)) as cursor:
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def create_translation_key(db: aiosqlite.Connection, 
                               key_name: str, 
                               category: str,
                               description: str,
                               translations: Dict[str, str]) -> int:
    """Create a new translation key with translations in multiple languages"""
    
    # Insert translation key
    cursor = await db.execute(
        "INSERT INTO translation_keys (key_name, category, description) VALUES (?, ?, ?)",
        (key_name, category, description)
    )
    key_id = cursor.lastrowid
    
    # Insert translations for each language
    for lang_code, text in translations.items():
        await db.execute(
            "INSERT INTO translations (translation_key_id, language_code, text, is_primary) VALUES (?, ?, ?, ?)",
            (key_id, lang_code, text, True)
        )
    
    await db.commit()
    return key_id

async def update_translation(db: aiosqlite.Connection, 
                           key_name: str, 
                           language_code: str, 
                           new_text: str) -> bool:
    """Update a translation"""
    cursor = await db.execute("""
        UPDATE translations 
        SET text = ? 
        WHERE translation_key_id = (
            SELECT id FROM translation_keys WHERE key_name = ?
        ) AND language_code = ?
    """, (new_text, key_name, language_code))
    
    await db.commit()
    return cursor.rowcount > 0

# Usage example function
async def example_create_exercise_with_translations(db: aiosqlite.Connection):
    """Example of how to create an exercise using the translation system"""
    
    exercise_data = {
        "question": "What type of word is 'كَتَبَ'?",
        "question_arabic": "ما نوع الكلمة 'كَتَبَ'؟",
        "exercise_type": "multiple_choice",
        "correct_answer": "فعل",
        "explanation": "كَتَبَ is a past tense verb meaning 'wrote'",
        "order": 1,
        "lesson_id": 1
    }
    
    options_data = [
        {"translation_key": "verb", "is_correct": True},
        {"translation_key": "noun", "is_correct": False},
        {"translation_key": "particle", "is_correct": False}
    ]
    
    exercise_id = await create_exercise_with_translated_options(db, exercise_data, options_data)
    return exercise_id
