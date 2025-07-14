import sqlite3
import random

def convert_fill_blank_to_multiple_choice():
    """Convert fill_blank exercises to multiple_choice by adding options"""
    conn = sqlite3.connect('nahw_exercises.db')
    cursor = conn.cursor()
    
    # Get all fill_blank exercises
    cursor.execute('SELECT id, question, question_arabic, correct_answer, explanation FROM exercises WHERE exercise_type = ?', ('fill_blank',))
    fill_blank_exercises = cursor.fetchall()
    
    print(f"Found {len(fill_blank_exercises)} fill_blank exercises to convert")
    
    for exercise_id, question, question_arabic, correct_answer, explanation in fill_blank_exercises:
        print(f"\nConverting exercise {exercise_id}: {question[:50]}...")
        
        # Update exercise type
        cursor.execute('UPDATE exercises SET exercise_type = ? WHERE id = ?', ('multiple_choice', exercise_id))
        
        # Create options for this exercise
        options = []
        
        # Add the correct answer
        options.append((exercise_id, correct_answer, True))
        
        # Add some plausible wrong answers based on the correct answer
        wrong_options = generate_wrong_options(correct_answer, question)
        for wrong_option in wrong_options:
            options.append((exercise_id, wrong_option, False))
        
        # Insert options into database
        cursor.executemany(
            'INSERT INTO exercise_options (exercise_id, option_text, is_correct) VALUES (?, ?, ?)',
            options
        )
        
        print(f"Added {len(options)} options for exercise {exercise_id}")
    
    conn.commit()
    conn.close()
    print(f"\nSuccessfully converted {len(fill_blank_exercises)} exercises!")

def generate_wrong_options(correct_answer, question):
    """Generate plausible wrong answers based on the correct answer and question context"""
    wrong_options = []
    
    # Arabic verb conjugations and common alternatives
    arabic_alternatives = {
        'يقرأ': ['قرأ', 'اقرأ', 'يقرأون'],
        'التُّفَّاحَةَ': ['التُّفَّاحَة', 'تُفَّاحَة', 'التُّفَّاح'],
        'يَكْتُبُ': ['كَتَبَ', 'اكتب', 'يكتبون'],
        'طَالِبٌ': ['طَالِب', 'الطَالِب', 'طُلَّاب'],
        'الأَطْفَالُ': ['الطِّفْل', 'أَطْفَال', 'طِفْل'],
        'الكِتَابَ': ['كِتَاب', 'الكِتَاب', 'كُتُب']
    }
    
    # Try to find alternatives for the correct answer
    if correct_answer in arabic_alternatives:
        wrong_options.extend(arabic_alternatives[correct_answer])
    else:
        # Generate generic alternatives based on patterns
        if correct_answer.startswith('ي'):  # Present tense verb
            wrong_options.extend([
                correct_answer.replace('ي', 'ت', 1),  # Change to feminine
                correct_answer.replace('ي', 'ن', 1),  # Change to plural
                correct_answer[1:] if len(correct_answer) > 1 else correct_answer  # Remove prefix
            ])
        elif correct_answer.startswith('ال'):  # Definite article
            wrong_options.extend([
                correct_answer[2:],  # Remove definite article
                correct_answer + 'ة',  # Add feminine marker
                correct_answer + 'ان'  # Add dual marker
            ])
        else:
            # Generic alternatives
            wrong_options.extend([
                'ال' + correct_answer,  # Add definite article
                correct_answer + 'ة',   # Add feminine marker
                correct_answer + 'ها'   # Add possessive pronoun
            ])
    
    # Remove duplicates and the correct answer, limit to 3 wrong options
    wrong_options = [opt for opt in wrong_options if opt != correct_answer and opt]
    return wrong_options[:3]

if __name__ == "__main__":
    convert_fill_blank_to_multiple_choice()
