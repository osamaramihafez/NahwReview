import asyncio
import aiosqlite
from typing import List, Dict, Optional

# Translation Helper Functions
class TranslationManager:
    def __init__(self, db_path: str = "nahw_exercises.db"):
        self.db_path = db_path
    
    async def get_translation(self, key_name: str, language_code: str = "ar") -> str:
        """Get translation for a key in specified language"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT t.text 
                FROM translations t
                JOIN translation_keys tk ON t.translation_key_id = tk.id
                WHERE tk.key_name = ? AND t.language_code = ? AND t.is_primary = 1
            """, (key_name, language_code)) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else key_name

    async def get_translation_key_id(self, key_name: str) -> Optional[int]:
        """Get translation key ID by key name"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT id FROM translation_keys WHERE key_name = ?", 
                (key_name,)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else None

    async def create_translation_key(self, key_name: str, category: str, 
                                   translations: Dict[str, str]) -> int:
        """Create a new translation key with translations in multiple languages"""
        async with aiosqlite.connect(self.db_path) as db:
            # Insert translation key
            cursor = await db.execute(
                "INSERT INTO translation_keys (key_name, category) VALUES (?, ?)",
                (key_name, category)
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

    async def get_exercise_options_localized(self, exercise_id: int, 
                                           language_code: str = "ar") -> List[Dict]:
        """Get exercise options with proper localization"""
        async with aiosqlite.connect(self.db_path) as db:
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

# Example Usage Functions
async def example_create_exercise_with_translations():
    """Example of creating an exercise using the translation system"""
    
    tm = TranslationManager()
    
    async with aiosqlite.connect("nahw_exercises.db") as db:
        print("📝 EXAMPLE: Creating Exercise with Translation System")
        print("=" * 55)
        
        # Example exercise data
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
        
        # Define options using translation keys
        options_with_keys = [
            {"translation_key": "verb", "is_correct": True},
            {"translation_key": "noun", "is_correct": False},
            {"translation_key": "particle", "is_correct": False}
        ]
        
        # Add options using translation keys
        for option in options_with_keys:
            key_id = await tm.get_translation_key_id(option["translation_key"])
            if key_id:
                await db.execute("""
                    INSERT INTO exercise_options 
                    (translation_key_id, is_correct, exercise_id) 
                    VALUES (?, ?, ?)
                """, (key_id, option["is_correct"], exercise_id))
                print(f"✅ Added option using translation key: {option['translation_key']}")
            else:
                print(f"❌ Translation key not found: {option['translation_key']}")
        
        await db.commit()
        
        # Demonstrate localization
        print("\n🌍 LOCALIZATION DEMO:")
        print("-" * 30)
        
        # Get options in Arabic
        arabic_options = await tm.get_exercise_options_localized(exercise_id, "ar")
        print("Arabic options:")
        for opt in arabic_options:
            print(f"  {'✓' if opt['is_correct'] else '✗'} {opt['option_text']}")
        
        # Get options in English
        english_options = await tm.get_exercise_options_localized(exercise_id, "en")
        print("\nEnglish options:")
        for opt in english_options:
            print(f"  {'✓' if opt['is_correct'] else '✗'} {opt['option_text']}")

async def example_bulk_translation_update():
    """Example of updating translations in bulk"""
    
    tm = TranslationManager()
    
    print("\n🔄 EXAMPLE: Bulk Translation Update")
    print("=" * 40)
    
    # Add French translations to existing keys
    french_translations = {
        "verb": "verbe",
        "noun": "nom", 
        "particle": "particule",
        "past_tense": "passé",
        "present_tense": "présent",
        "nominative": "nominatif",
        "accusative": "accusatif"
    }
    
    async with aiosqlite.connect("nahw_exercises.db") as db:
        for key_name, french_text in french_translations.items():
            # Get the translation key ID
            key_id = await tm.get_translation_key_id(key_name)
            if key_id:
                # Add French translation
                await db.execute("""
                    INSERT OR IGNORE INTO translations 
                    (translation_key_id, language_code, text, is_primary) 
                    VALUES (?, ?, ?, ?)
                """, (key_id, "fr", french_text, True))
                print(f"✅ Added French translation: {key_name} -> {french_text}")
        
        await db.commit()
        print("🎉 Bulk French translations added!")

async def example_admin_interface_functions():
    """Example functions for an admin translation management interface"""
    
    print("\n🛠️  ADMIN INTERFACE FUNCTIONS")
    print("=" * 40)
    
    admin_functions = '''
# These functions would be used in an admin interface

async def get_all_translation_keys_with_stats(db):
    """Get all translation keys with usage statistics"""
    async with db.execute("""
        SELECT 
            tk.id,
            tk.key_name,
            tk.category,
            COUNT(DISTINCT t.language_code) as language_count,
            COUNT(DISTINCT eo.exercise_id) as usage_count
        FROM translation_keys tk
        LEFT JOIN translations t ON tk.id = t.translation_key_id
        LEFT JOIN exercise_options eo ON tk.id = eo.translation_key_id
        GROUP BY tk.id, tk.key_name, tk.category
        ORDER BY usage_count DESC
    """) as cursor:
        return await cursor.fetchall()

async def get_missing_translations(db, language_code):
    """Find translation keys missing translations for a specific language"""
    async with db.execute("""
        SELECT tk.key_name, tk.category
        FROM translation_keys tk
        WHERE tk.id NOT IN (
            SELECT DISTINCT translation_key_id 
            FROM translations 
            WHERE language_code = ?
        )
        ORDER BY tk.category, tk.key_name
    """, (language_code,)) as cursor:
        return await cursor.fetchall()

async def update_translation(db, key_name, language_code, new_text):
    """Update a translation"""
    await db.execute("""
        UPDATE translations 
        SET text = ? 
        WHERE translation_key_id = (
            SELECT id FROM translation_keys WHERE key_name = ?
        ) AND language_code = ?
    """, (new_text, key_name, language_code))
    await db.commit()

async def get_translation_usage_report(db):
    """Generate a report showing which translations are most used"""
    async with db.execute("""
        SELECT 
            tk.key_name,
            tk.category,
            COUNT(eo.id) as option_usage,
            GROUP_CONCAT(DISTINCT t.language_code) as available_languages
        FROM translation_keys tk
        LEFT JOIN exercise_options eo ON tk.id = eo.translation_key_id
        LEFT JOIN translations t ON tk.id = t.translation_key_id
        GROUP BY tk.id
        ORDER BY option_usage DESC
    """) as cursor:
        return await cursor.fetchall()
'''
    
    print(admin_functions)

async def demonstrate_complete_workflow():
    """Demonstrate the complete workflow with the translation system"""
    
    print("\n🚀 COMPLETE WORKFLOW DEMONSTRATION")
    print("=" * 50)
    
    workflow = '''
STEP 1: Setup Translation System
✅ Create translation_keys table
✅ Create translations table  
✅ Create updated exercise_options table
✅ Populate common grammatical terms

STEP 2: Create New Exercise (Developer)
```python
exercise_data = {
    "question": "Identify the grammatical case",
    "question_arabic": "عيّن حالة الإعراب", 
    "options": [
        {"translation_key": "nominative", "is_correct": True},
        {"translation_key": "accusative", "is_correct": False},
        {"translation_key": "genitive", "is_correct": False}
    ]
}
```

STEP 3: User Interface (Frontend)
- User selects language preference
- API returns localized options based on language
- All users see consistent terminology

STEP 4: Admin Management
- Add new languages easily
- Update terminology in one place
- Monitor translation coverage
- Generate usage reports

BENEFITS ACHIEVED:
✅ No more duplicate translations
✅ Consistent terminology across app
✅ Easy to add new languages
✅ Centralized translation management
✅ Reduced database size
✅ Better maintainability
'''
    
    print(workflow)

async def run_complete_example():
    """Run the complete example"""
    
    # First ensure we have the translation system set up
    print("Setting up translation system...")
    
    # This would run the create_translation_system.py first
    print("(Run create_translation_system.py first to set up tables)")
    
    # Then demonstrate usage
    await example_create_exercise_with_translations()
    await example_bulk_translation_update()
    await example_admin_interface_functions()
    await demonstrate_complete_workflow()

if __name__ == "__main__":
    print("🎯 COMPREHENSIVE TRANSLATION SYSTEM EXAMPLE")
    print("=" * 60)
    asyncio.run(run_complete_example())
