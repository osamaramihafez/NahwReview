import asyncio
import aiosqlite

async def fix_english_translations():
    """Fix English translations to show proper English terms"""
    
    async with aiosqlite.connect("nahw_exercises.db") as db:
        
        print("🔧 FIXING ENGLISH TRANSLATIONS")
        print("=" * 35)
        
        # Proper English translations for grammatical terms
        english_translations = {
            "verb": "verb",
            "noun": "noun", 
            "particle": "particle",
            "past_tense": "past",
            "present_tense": "present",
            "imperative": "imperative",
            "nominative": "nominative",
            "accusative": "accusative",
            "genitive": "genitive",
            "jussive": "jussive",
            "subject_doer": "doer/subject",
            "direct_object": "direct object",
            "subject_nominal": "subject",
            "predicate": "predicate",
            "verbal_sentence": "verbal sentence",
            "nominal_sentence": "nominal sentence",
            "visible_damma": "visible damma",
            "visible_fatha": "visible fatha",
            "visible_kasra": "visible kasra",
            "built_on_fath": "built on fatha",
            "built_on_damma": "built on damma",
            "built_on_sukun": "built on sukun"
        }
        
        for key_name, english_text in english_translations.items():
            # Update English translation
            cursor = await db.execute("""
                UPDATE translations 
                SET text = ? 
                WHERE translation_key_id = (
                    SELECT id FROM translation_keys WHERE key_name = ?
                ) AND language_code = 'en'
            """, (english_text, key_name))
            
            if cursor.rowcount > 0:
                print(f"✅ Updated '{key_name}' English translation to '{english_text}'")
        
        await db.commit()
        print(f"\n🎉 English translations updated!")

if __name__ == "__main__":
    asyncio.run(fix_english_translations())
