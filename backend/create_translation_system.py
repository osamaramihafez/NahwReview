import asyncio
import aiosqlite

async def create_translation_system():
    """Create a modular translation system for the Nahw Exercises app"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        
        # Create translation_keys table - the main reference table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS translation_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_name TEXT UNIQUE NOT NULL,
                category TEXT, -- 'grammatical_term', 'option', 'common_phrase', etc.
                description TEXT
            )
        """)
        
        # Create translations table - stores actual translations
        await db.execute("""
            CREATE TABLE IF NOT EXISTS translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                translation_key_id INTEGER NOT NULL,
                language_code TEXT NOT NULL, -- 'en', 'ar', etc.
                text TEXT NOT NULL,
                is_primary BOOLEAN DEFAULT 0, -- for cases with multiple translations
                FOREIGN KEY (translation_key_id) REFERENCES translation_keys (id),
                UNIQUE(translation_key_id, language_code, text)
            )
        """)
        
        # Create updated exercise_options table with translation reference
        await db.execute("""
            CREATE TABLE IF NOT EXISTS exercise_options_v2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                translation_key_id INTEGER, -- References translation_keys
                option_text TEXT, -- Fallback for options that don't need translation
                is_correct BOOLEAN DEFAULT 0,
                exercise_id INTEGER NOT NULL,
                FOREIGN KEY (translation_key_id) REFERENCES translation_keys (id),
                FOREIGN KEY (exercise_id) REFERENCES exercises (id)
            )
        """)
        
        await db.commit()
        print("✅ Translation system tables created successfully!")

async def populate_common_grammatical_terms():
    """Populate the translation system with common grammatical terms"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        
        # Common grammatical terms that appear frequently in exercises
        grammatical_terms = [
            # Parts of speech
            {"key": "noun", "en": "اسم", "ar": "اسم", "category": "parts_of_speech"},
            {"key": "verb", "en": "فعل", "ar": "فعل", "category": "parts_of_speech"},
            {"key": "particle", "en": "حرف", "ar": "حرف", "category": "parts_of_speech"},
            
            # Verb tenses
            {"key": "past_tense", "en": "ماض", "ar": "ماض", "category": "verb_tense"},
            {"key": "present_tense", "en": "مضارع", "ar": "مضارع", "category": "verb_tense"},
            {"key": "imperative", "en": "أمر", "ar": "أمر", "category": "verb_tense"},
            
            # Grammatical cases
            {"key": "nominative", "en": "مرفوع", "ar": "مرفوع", "category": "grammatical_case"},
            {"key": "accusative", "en": "منصوب", "ar": "منصوب", "category": "grammatical_case"},
            {"key": "genitive", "en": "مجرور", "ar": "مجرور", "category": "grammatical_case"},
            {"key": "jussive", "en": "مجزوم", "ar": "مجزوم", "category": "grammatical_case"},
            
            # Sentence elements
            {"key": "subject_doer", "en": "فاعل", "ar": "فاعل", "category": "sentence_element"},
            {"key": "direct_object", "en": "مفعول به", "ar": "مفعول به", "category": "sentence_element"},
            {"key": "subject_nominal", "en": "مبتدأ", "ar": "مبتدأ", "category": "sentence_element"},
            {"key": "predicate", "en": "خبر", "ar": "خبر", "category": "sentence_element"},
            
            # Grammatical constructions
            {"key": "verbal_sentence", "en": "جملة فعلية", "ar": "جملة فعلية", "category": "sentence_type"},
            {"key": "nominal_sentence", "en": "جملة اسمية", "ar": "جملة اسمية", "category": "sentence_type"},
            
            # Signs of inflection
            {"key": "visible_damma", "en": "الضمة الظاهرة", "ar": "الضمة الظاهرة", "category": "inflection_sign"},
            {"key": "visible_fatha", "en": "الفتحة الظاهرة", "ar": "الفتحة الظاهرة", "category": "inflection_sign"},
            {"key": "visible_kasra", "en": "الكسرة الظاهرة", "ar": "الكسرة الظاهرة", "category": "inflection_sign"},
            
            # Construction phrases
            {"key": "built_on_fath", "en": "مبني على الفتح", "ar": "مبني على الفتح", "category": "construction"},
            {"key": "built_on_damma", "en": "مبني على الضم", "ar": "مبني على الضم", "category": "construction"},
            {"key": "built_on_sukun", "en": "مبني على السكون", "ar": "مبني على السكون", "category": "construction"},
        ]
        
        for term in grammatical_terms:
            # Insert translation key
            cursor = await db.execute(
                "INSERT OR IGNORE INTO translation_keys (key_name, category) VALUES (?, ?)",
                (term["key"], term["category"])
            )
            
            # Get the key ID
            key_cursor = await db.execute(
                "SELECT id FROM translation_keys WHERE key_name = ?", 
                (term["key"],)
            )
            key_row = await key_cursor.fetchone()
            if key_row:
                key_id = key_row[0]
                
                # Insert English translation
                await db.execute(
                    "INSERT OR IGNORE INTO translations (translation_key_id, language_code, text, is_primary) VALUES (?, ?, ?, ?)",
                    (key_id, "en", term["en"], True)
                )
                
                # Insert Arabic translation
                await db.execute(
                    "INSERT OR IGNORE INTO translations (translation_key_id, language_code, text, is_primary) VALUES (?, ?, ?, ?)",
                    (key_id, "ar", term["ar"], True)
                )
        
        await db.commit()
        print(f"✅ Populated {len(grammatical_terms)} grammatical terms in translation system!")

async def create_translation_functions():
    """Create helper functions for working with translations"""
    
    # This would be implemented in your main code/crud.py
    function_code = '''
# Add these functions to your crud.py or create a new translations.py file

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

async def get_translation_key_id(db: aiosqlite.Connection, key_name: str) -> int:
    """Get translation key ID by key name"""
    async with db.execute(
        "SELECT id FROM translation_keys WHERE key_name = ?", 
        (key_name,)
    ) as cursor:
        row = await cursor.fetchone()
        return row[0] if row else None

async def create_exercise_option_with_translation(db: aiosqlite.Connection, 
                                                exercise_id: int, 
                                                translation_key: str, 
                                                is_correct: bool):
    """Create exercise option using translation key"""
    key_id = await get_translation_key_id(db, translation_key)
    if key_id:
        await db.execute(
            "INSERT INTO exercise_options_v2 (translation_key_id, is_correct, exercise_id) VALUES (?, ?, ?)",
            (key_id, is_correct, exercise_id)
        )
    else:
        print(f"Warning: Translation key '{translation_key}' not found")

async def get_exercise_options_with_translations(db: aiosqlite.Connection, 
                                               exercise_id: int, 
                                               language_code: str = "ar") -> List[Dict]:
    """Get exercise options with translations in specified language"""
    async with db.execute("""
        SELECT 
            eo.id,
            eo.is_correct,
            COALESCE(t.text, eo.option_text) as option_text,
            tk.key_name
        FROM exercise_options_v2 eo
        LEFT JOIN translation_keys tk ON eo.translation_key_id = tk.id
        LEFT JOIN translations t ON tk.id = t.translation_key_id AND t.language_code = ? AND t.is_primary = 1
        WHERE eo.exercise_id = ?
        ORDER BY eo.id
    """, (language_code, exercise_id)) as cursor:
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
'''
    
    print("🔧 Translation helper functions:")
    print(function_code)

async def demonstrate_usage():
    """Demonstrate how to use the translation system"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        
        print("\n📝 Example: Creating exercise options with translations")
        print("Instead of:")
        print("  INSERT INTO exercise_options (option_text, is_correct, exercise_id) VALUES ('فعل', True, 1)")
        print("  INSERT INTO exercise_options (option_text, is_correct, exercise_id) VALUES ('اسم', False, 1)")
        
        print("\nYou would do:")
        print("  INSERT INTO exercise_options_v2 (translation_key_id, is_correct, exercise_id) VALUES")
        print("    ((SELECT id FROM translation_keys WHERE key_name = 'verb'), True, 1),")
        print("    ((SELECT id FROM translation_keys WHERE key_name = 'noun'), False, 1)")
        
        print("\n🌍 Benefits:")
        print("  1. Consistent translations across the app")
        print("  2. Easy to add new languages")
        print("  3. Centralized terminology management")
        print("  4. Reduced database size")
        print("  5. Easy bulk translation updates")

async def migration_plan():
    """Show how to migrate existing data to the new system"""
    migration_steps = '''
    
📋 MIGRATION PLAN:

1. **Create New Tables** (Done above)
   - translation_keys
   - translations  
   - exercise_options_v2

2. **Populate Common Terms** (Done above)
   - Grammatical terms
   - Common phrases
   - Sentence elements

3. **Migrate Existing Options:**
   ```sql
   -- Find unique option texts that can be translated
   SELECT DISTINCT option_text, COUNT(*) as usage_count 
   FROM exercise_options 
   GROUP BY option_text 
   ORDER BY usage_count DESC;
   
   -- Create translation keys for common options
   -- Migrate exercise_options to exercise_options_v2
   ```

4. **Update Application Code:**
   - Modify API endpoints to use translation system
   - Update frontend to handle language switching
   - Add translation management interface

5. **Testing:**
   - Verify all options display correctly
   - Test language switching
   - Validate data integrity
   '''
    print(migration_steps)

if __name__ == "__main__":
    print("🚀 Creating Translation System for Nahw Exercises")
    print("=" * 60)
    
    asyncio.run(create_translation_system())
    asyncio.run(populate_common_grammatical_terms())
    asyncio.run(create_translation_functions())
    asyncio.run(demonstrate_usage())
    asyncio.run(migration_plan())
