import requests
import json

def test_irab_analysis_exercise():
    """Test the new irab analysis exercise functionality"""
    base_url = "http://localhost:8000"
    
    # Test getting exercises for lesson 1 (should include our irab analysis exercise)
    print("Testing irab analysis exercise...")
    
    try:
        response = requests.get(f"{base_url}/lessons/1/exercises")
        if response.status_code == 200:
            exercises = response.json()
            
            # Find irab analysis exercises
            irab_exercises = [ex for ex in exercises if ex['exercise_type'] == 'irab_analysis']
            
            print(f"Found {len(irab_exercises)} irab analysis exercises in lesson 1")
            
            for exercise in irab_exercises:
                print(f"\nExercise ID: {exercise['id']}")
                print(f"Question: {exercise['question']}")
                print(f"Arabic: {exercise['question_arabic']}")
                print(f"Type: {exercise['exercise_type']}")
                
                # Parse the exercise data
                try:
                    data = json.loads(exercise['correct_answer'])
                    print(f"Sentence: {data['sentence']}")
                    print(f"Number of words: {len(data['words'])}")
                    
                    for i, word in enumerate(data['words']):
                        print(f"  Word {i+1}: {word['text']} - {len(word.get('questions', []))} questions")
                        
                except Exception as e:
                    print(f"Error parsing exercise data: {e}")
                
                # Test checking an answer
                print(f"\nTesting answer check for exercise {exercise['id']}...")
                answer_response = requests.post(
                    f"{base_url}/exercises/{exercise['id']}/check",
                    json={
                        "user_answer": "تم إكمال التحليل النحوي بنجاح - النتيجة: 85%",
                        "user_id": "test_user"
                    }
                )
                
                if answer_response.status_code == 200:
                    result = answer_response.json()
                    print(f"Answer check result: {result}")
                else:
                    print(f"Error checking answer: {answer_response.status_code}")
        else:
            print(f"Error getting exercises: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to backend. Make sure the server is running.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_irab_analysis_exercise()
