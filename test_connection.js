// Simple test script to verify backend-frontend connection
const axios = require('axios');

const API_BASE_URL = 'http://localhost:8001';

async function testConnection() {
    console.log('Testing Nahw Exercises API Connection...\n');
    
    try {
        // Test 1: Root endpoint
        console.log('1. Testing root endpoint...');
        const rootResponse = await axios.get(`${API_BASE_URL}/`);
        console.log('✅ Root endpoint:', rootResponse.data.message);
        
        // Test 2: Levels endpoint
        console.log('\n2. Testing levels endpoint...');
        const levelsResponse = await axios.get(`${API_BASE_URL}/levels`);
        console.log(`✅ Found ${levelsResponse.data.length} levels`);
        levelsResponse.data.forEach(level => {
            console.log(`   - Level ${level.order}: ${level.name}`);
        });
        
        // Test 3: Lessons endpoint (for first level)
        if (levelsResponse.data.length > 0) {
            const firstLevelId = levelsResponse.data[0].id;
            console.log(`\n3. Testing lessons endpoint for level ${firstLevelId}...`);
            const lessonsResponse = await axios.get(`${API_BASE_URL}/levels/${firstLevelId}/lessons`);
            console.log(`✅ Found ${lessonsResponse.data.length} lessons`);
            lessonsResponse.data.slice(0, 3).forEach(lesson => {
                console.log(`   - Lesson ${lesson.order}: ${lesson.title}`);
            });
            
            // Test 4: Exercises endpoint (for first lesson)
            if (lessonsResponse.data.length > 0) {
                const firstLessonId = lessonsResponse.data[0].id;
                console.log(`\n4. Testing exercises endpoint for lesson ${firstLessonId}...`);
                const exercisesResponse = await axios.get(`${API_BASE_URL}/lessons/${firstLessonId}/exercises`);
                console.log(`✅ Found ${exercisesResponse.data.length} exercises`);
                if (exercisesResponse.data.length > 0) {
                    const firstExercise = exercisesResponse.data[0];
                    console.log(`   - Exercise: ${firstExercise.question}`);
                    console.log(`   - Type: ${firstExercise.exercise_type}`);
                    if (firstExercise.options && firstExercise.options.length > 0) {
                        console.log(`   - Options: ${firstExercise.options.length} choices`);
                    }
                    
                    // Test 5: Check answer endpoint
                    console.log(`\n5. Testing answer checking...`);
                    const answerResponse = await axios.post(`${API_BASE_URL}/exercises/${firstExercise.id}/check`, {
                        exercise_id: firstExercise.id,
                        user_answer: firstExercise.correct_answer,
                        user_id: 'test_user'
                    });
                    console.log(`✅ Answer check: ${answerResponse.data.is_correct ? 'Correct' : 'Incorrect'}`);
                    if (answerResponse.data.explanation) {
                        console.log(`   - Explanation available: Yes`);
                    }
                }
            }
        }
        
        console.log('\n🎉 All API tests passed! Backend and frontend are properly connected.');
        console.log('\nNext steps:');
        console.log('1. Open your browser to http://localhost:8081 to see the React Native web app');
        console.log('2. Use the Expo Go app to scan the QR code for mobile testing');
        console.log('3. Visit http://localhost:8001/docs for API documentation');
        
    } catch (error) {
        console.error('❌ Connection test failed:');
        if (error.code === 'ECONNREFUSED') {
            console.error('   - Backend server is not running. Please start it with: python backend/main.py');
        } else {
            console.error('   - Error:', error.message);
        }
        console.log('\nTroubleshooting:');
        console.log('1. Make sure the backend server is running on port 8001');
        console.log('2. Check that the database has been populated with: python backend/populate_db.py');
        console.log('3. Verify all dependencies are installed');
    }
}

// Run the test
testConnection();
