import asyncio
import aiosqlite
import json

async def analyze_existing_options():
    """Analyze existing exercise options to identify translation candidates"""
    async with aiosqlite.connect("nahw_exercises.db") as db:
        
        print("📊 ANALYZING EXISTING EXERCISE OPTIONS")
        print("=" * 50)
        
        # Get all unique option texts and their usage frequency
        async with db.execute("""
            SELECT option_text, COUNT(*) as usage_count, 
                   GROUP_CONCAT(DISTINCT exercise_id) as exercise_ids
            FROM exercise_options 
            GROUP BY option_text 
            ORDER BY usage_count DESC
        """) as cursor:
            options = await cursor.fetchall()
        
        print(f"Found {len(options)} unique option texts")
        print("\n🔤 Most frequently used options:")
        print("-" * 40)
        
        # Categorize options
        grammatical_terms = []
        arabic_words = []
        english_phrases = []
        mixed_phrases = []
        
        for option_text, count, exercise_ids in options[:20]:  # Top 20
            print(f"{option_text:<25} | Used {count:>2} times | Exercises: {exercise_ids[:50]}{'...' if len(exercise_ids) > 50 else ''}")
            
            # Categorize based on content
            if any(arabic_char in option_text for arabic_char in 'ابتثجحخدذرزسشصضطظعغفقكلمنهوي'):
                if any(english_char.isalpha() and ord(english_char) < 128 for english_char in option_text):
                    mixed_phrases.append((option_text, count))
                else:
                    arabic_words.append((option_text, count))
            else:
                english_phrases.append((option_text, count))
        
        print(f"\n📈 CATEGORIZATION:")
        print(f"Arabic terms: {len(arabic_words)}")
        print(f"English phrases: {len(english_phrases)}")
        print(f"Mixed phrases: {len(mixed_phrases)}")
        
        return {
            'arabic_terms': arabic_words,
            'english_phrases': english_phrases,
            'mixed_phrases': mixed_phrases,
            'all_options': options
        }

async def create_translation_keys_from_analysis():
    """Create translation keys for commonly used options"""
    
    # First analyze existing options
    analysis = await analyze_existing_options()
    
    async with aiosqlite.connect("nahw_exercises.db") as db:
        
        print("\n🔧 CREATING TRANSLATION KEYS FROM ANALYSIS")
        print("=" * 50)
        
        # Arabic grammatical terms that should become translation keys
        common_arabic_terms = [
            'فعل', 'اسم', 'حرف', 'ماض', 'مضارع', 'أمر',
            'مرفوع', 'منصوب', 'مجرور', 'مجزوم',
            'فاعل', 'مفعول به', 'مبتدأ', 'خبر',
            'الضمة الظاهرة', 'الفتحة الظاهرة', 'الكسرة الظاهرة',
            'مبني على الفتح', 'مبني على الضم', 'مبني على السكون'
        ]
        
        created_keys = 0
        
        for arabic_term, count in analysis['arabic_terms']:
            if arabic_term in common_arabic_terms:
                # Create translation key
                key_name = f"term_{arabic_term.replace(' ', '_').replace('ال', '')}"
                
                try:
                    # Insert translation key
                    await db.execute(
                        "INSERT OR IGNORE INTO translation_keys (key_name, category, description) VALUES (?, ?, ?)",
                        (key_name, "grammatical_term", f"Common term used {count} times")
                    )
                    
                    # Get the key ID
                    async with db.execute(
                        "SELECT id FROM translation_keys WHERE key_name = ?", 
                        (key_name,)
                    ) as cursor:
                        key_row = await cursor.fetchone()
                        if key_row:
                            key_id = key_row[0]
                            
                            # Insert Arabic translation
                            await db.execute(
                                "INSERT OR IGNORE INTO translations (translation_key_id, language_code, text, is_primary) VALUES (?, ?, ?, ?)",
                                (key_id, "ar", arabic_term, True)
                            )
                            
                            # Add English translation where known
                            english_translation = get_english_equivalent(arabic_term)
                            if english_translation:
                                await db.execute(
                                    "INSERT OR IGNORE INTO translations (translation_key_id, language_code, text, is_primary) VALUES (?, ?, ?, ?)",
                                    (key_id, "en", english_translation, True)
                                )
                            
                            created_keys += 1
                            print(f"✅ Created key '{key_name}' for '{arabic_term}' (used {count} times)")
                
                except Exception as e:
                    print(f"❌ Error creating key for '{arabic_term}': {e}")
        
        await db.commit()
        print(f"\n🎉 Created {created_keys} translation keys from existing options!")

def get_english_equivalent(arabic_term):
    """Get English equivalent for common Arabic grammatical terms"""
    translations = {
        'فعل': 'verb',
        'اسم': 'noun', 
        'حرف': 'particle',
        'ماض': 'past',
        'مضارع': 'present',
        'أمر': 'imperative',
        'مرفوع': 'nominative',
        'منصوب': 'accusative',
        'مجرور': 'genitive',
        'مجزوم': 'jussive',
        'فاعل': 'doer/subject',
        'مفعول به': 'direct object',
        'مبتدأ': 'subject',
        'خبر': 'predicate',
        'الضمة الظاهرة': 'visible damma',
        'الفتحة الظاهرة': 'visible fatha',
        'الكسرة الظاهرة': 'visible kasra',
        'مبني على الفتح': 'built on fatha',
        'مبني على الضم': 'built on damma',
        'مبني على السكون': 'built on sukun'
    }
    return translations.get(arabic_term)

async def migrate_exercise_options():
    """Migrate existing exercise_options to use translation system where possible"""
    
    async with aiosqlite.connect("nahw_exercises.db") as db:
        
        print("\n🔄 MIGRATING EXERCISE OPTIONS")
        print("=" * 40)
        
        # Get all existing options
        async with db.execute("""
            SELECT id, option_text, is_correct, exercise_id 
            FROM exercise_options
        """) as cursor:
            existing_options = await cursor.fetchall()
        
        migrated_count = 0
        fallback_count = 0
        
        for option_id, option_text, is_correct, exercise_id in existing_options:
            
            # Try to find a translation key for this option
            async with db.execute("""
                SELECT tk.id 
                FROM translation_keys tk
                JOIN translations t ON tk.id = t.translation_key_id
                WHERE t.text = ? AND t.language_code = 'ar'
            """, (option_text,)) as cursor:
                key_row = await cursor.fetchone()
            
            if key_row:
                # Found translation key - use it
                translation_key_id = key_row[0]
                await db.execute("""
                    INSERT INTO exercise_options_v2 
                    (translation_key_id, is_correct, exercise_id) 
                    VALUES (?, ?, ?)
                """, (translation_key_id, is_correct, exercise_id))
                migrated_count += 1
            else:
                # No translation key found - fallback to direct text
                await db.execute("""
                    INSERT INTO exercise_options_v2 
                    (option_text, is_correct, exercise_id) 
                    VALUES (?, ?, ?)
                """, (option_text, is_correct, exercise_id))
                fallback_count += 1
        
        await db.commit()
        
        print(f"✅ Migration complete!")
        print(f"   📝 {migrated_count} options migrated with translation keys")
        print(f"   📝 {fallback_count} options kept as direct text")
        print(f"   📊 {migrated_count/(migrated_count+fallback_count)*100:.1f}% using translation system")

async def create_api_helper_functions():
    """Create helper functions for the API to use translations"""
    
    helper_code = '''
# Add these functions to your crud.py

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
        FROM exercise_options_v2 eo
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
                    INSERT INTO exercise_options_v2 
                    (translation_key_id, is_correct, exercise_id) 
                    VALUES (?, ?, ?)
                """, (key_id, option["is_correct"], exercise_id))
            else:
                print(f"Warning: Translation key '{option['translation_key']}' not found")
        else:
            # Fallback to direct text
            await db.execute("""
                INSERT INTO exercise_options_v2 
                (option_text, is_correct, exercise_id) 
                VALUES (?, ?, ?)
            """, (option["option_text"], option["is_correct"], exercise_id))
    
    await db.commit()
    return exercise_id

async def get_all_translations(db: aiosqlite.Connection, language_code: str = "ar") -> Dict[str, str]:
    """Get all translations for a language as a key-value dict"""
    
    async with db.execute("""
        SELECT tk.key_name, t.text
        FROM translation_keys tk
        JOIN translations t ON tk.id = t.translation_key_id
        WHERE t.language_code = ? AND t.is_primary = 1
    """, (language_code,)) as cursor:
        rows = await cursor.fetchall()
        return {row[0]: row[1] for row in rows}
'''
    
    print("\n🔧 API HELPER FUNCTIONS:")
    print("Save this to a new file: backend/translation_helpers.py")
    print(helper_code)

async def demonstrate_new_workflow():
    """Show the new workflow for creating exercises"""
    
    example = '''
📚 NEW WORKFLOW EXAMPLE:

OLD WAY (storing both languages everywhere):
```python
exercise_data = {
    "question": "What type of word is this?",
    "question_arabic": "ما نوع هذه الكلمة؟",
    "options": [
        {"option_text": "فعل", "is_correct": True},
        {"option_text": "اسم", "is_correct": False}, 
        {"option_text": "حرف", "is_correct": False}
    ]
}
```

NEW WAY (using translation keys):
```python
exercise_data = {
    "question": "What type of word is this?",
    "question_arabic": "ما نوع هذه الكلمة؟",
    "options": [
        {"translation_key": "verb", "is_correct": True},
        {"translation_key": "noun", "is_correct": False},
        {"translation_key": "particle", "is_correct": False}
    ]
}
```

BENEFITS:
✅ Consistent terminology across all exercises
✅ Easy to add new languages (French, Spanish, etc.)
✅ Centralized translation management
✅ Smaller database size
✅ No duplicate translation work
✅ Easy bulk updates to terminology

LANGUAGE SWITCHING:
- User selects Arabic: options show "فعل", "اسم", "حرف"
- User selects English: options show "verb", "noun", "particle"
- User selects French: options show "verbe", "nom", "particule" (when added)
'''
    print(example)

if __name__ == "__main__":
    print("🔄 MIGRATION SCRIPT FOR TRANSLATION SYSTEM")
    print("=" * 60)
    
    async def run_migration():
        await analyze_existing_options()
        await create_translation_keys_from_analysis()
        await migrate_exercise_options()
        await create_api_helper_functions()
        await demonstrate_new_workflow()
        
        print("\n✅ MIGRATION COMPLETE!")
        print("Next steps:")
        print("1. Test the new exercise_options_v2 table")
        print("2. Update your API endpoints to use translation system")
        print("3. Add language switching to frontend")
        print("4. Create admin interface for managing translations")
    
    asyncio.run(run_migration())
