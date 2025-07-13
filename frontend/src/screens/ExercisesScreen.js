import React, { useState, useEffect } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  FlatList, 
  ActivityIndicator,
  Alert,
  TouchableOpacity 
} from 'react-native';
import { lessonsAPI, exercisesAPI, levelsAPI } from '../services/api';
import ExerciseCard from '../components/ExerciseCard';

const ExercisesScreen = ({ route, navigation }) => {
  const { lesson } = route.params;
  const [exercises, setExercises] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [completed, setCompleted] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);
  const [canGoNext, setCanGoNext] = useState(false);

  useEffect(() => {
    fetchExercises();
  }, []);

  const fetchExercises = async () => {
    try {
      const response = await lessonsAPI.getExercises(lesson.id);
      setExercises(response.data);
    } catch (error) {
      console.error('Error fetching exercises:', error);
      Alert.alert('Error', 'Failed to load exercises. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = async (userAnswer) => {
    const currentExercise = exercises[currentExerciseIndex];
    
    try {
      const response = await exercisesAPI.checkAnswer(
        currentExercise.id, 
        userAnswer,
        'default_user' // TODO: Implement proper user management
      );
      
      if (response.data.is_correct) {
        setScore(score + 1);
      }

      setShowExplanation(true);
      setCanGoNext(true);

    } catch (error) {
      console.error('Error checking answer:', error);
      Alert.alert('Error', 'Failed to check answer. Please try again.');
    }
  };

  const goToNextExercise = async () => {
    console.log('goToNextExercise called', { currentExerciseIndex, exercisesLength: exercises.length });
    setShowExplanation(false);
    setCanGoNext(false);
    
    if (currentExerciseIndex < exercises.length - 1) {
      setCurrentExerciseIndex(currentExerciseIndex + 1);
    } else {
      // Last exercise completed
      console.log('Last exercise completed, showing completion dialog');
      await showCompletionDialog();
    }
  };

  const goToPreviousExercise = () => {
    if (currentExerciseIndex > 0) {
      setShowExplanation(false);
      setCanGoNext(false);
      setCurrentExerciseIndex(currentExerciseIndex - 1);
    }
  };

  const showCompletionDialog = async () => {
    const percentage = Math.round((score / exercises.length) * 100);
    
    // Simple completion dialog that always works
    const showSimpleCompletion = () => {
      Alert.alert(
        'Lesson Complete!',
        `You scored ${score}/${exercises.length} (${percentage}%)`,
        [
          { 
            text: 'Review', 
            onPress: () => {
              setCurrentExerciseIndex(0);
              setShowExplanation(false);
              setCanGoNext(false);
            }
          },
          { text: 'Back to Lessons', onPress: () => navigation.goBack() }
        ]
      );
    };

    try {
      // Try to get the next lesson
      const nextLessonResponse = await lessonsAPI.getNextLesson(lesson.id);
      const nextLesson = nextLessonResponse.data;
      
      Alert.alert(
        'Lesson Complete!',
        `You scored ${score}/${exercises.length} (${percentage}%)\n\nWould you like to continue to the next lesson?`,
        [
          { 
            text: 'Review', 
            onPress: () => {
              setCurrentExerciseIndex(0);
              setShowExplanation(false);
              setCanGoNext(false);
            }
          },
          { text: 'Back to Lessons', onPress: () => navigation.goBack() },
          { 
            text: 'Next Lesson', 
            onPress: () => navigation.replace('Exercises', { lesson: nextLesson }) 
          }
        ]
      );
    } catch (error) {
      console.log('No next lesson found, trying next level...', error);
      // No next lesson in current level, try next level
      try {
        const nextLevelResponse = await levelsAPI.getNextLevel(lesson.level_id);
        const nextLevel = nextLevelResponse.data;
        
        Alert.alert(
          'Level Complete!',
          `You scored ${score}/${exercises.length} (${percentage}%)\n\nYou've completed this level! Continue to the next level?`,
          [
            { 
              text: 'Review', 
              onPress: () => {
                setCurrentExerciseIndex(0);
                setShowExplanation(false);
                setCanGoNext(false);
              }
            },
            { text: 'Back to Lessons', onPress: () => navigation.goBack() },
            { 
              text: 'Next Level', 
              onPress: () => {
                // Navigate back to the lessons screen and then to the new level
                navigation.navigate('Lessons', { level: nextLevel });
              }
            }
          ]
        );
      } catch (levelError) {
        console.log('No next level found or API error, showing simple completion', levelError);
        // Fallback to simple completion if API calls fail
        showSimpleCompletion();
      }
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2E8B57" />
        <Text style={styles.loadingText}>Loading exercises...</Text>
      </View>
    );
  }

  if (exercises.length === 0) {
    return (
      <View style={styles.emptyContainer}>
        <Text style={styles.emptyText}>No exercises available for this lesson.</Text>
        <TouchableOpacity 
          style={styles.backButton} 
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.backButtonText}>Go Back</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const currentExercise = exercises[currentExerciseIndex];

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity 
          style={styles.headerBackButton} 
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.headerBackButtonText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.title}>{lesson.title}</Text>
        {lesson.arabic_title && (
          <Text style={styles.arabicTitle}>{lesson.arabic_title}</Text>
        )}
        <View style={styles.progressContainer}>
          <Text style={styles.progressText}>
            Exercise {currentExerciseIndex + 1} of {exercises.length}
          </Text>
          <Text style={styles.scoreText}>Score: {score}/{exercises.length}</Text>
        </View>
      </View>

      <View style={styles.exerciseContainer}>
        <ExerciseCard 
          exercise={currentExercise}
          onAnswer={handleAnswer}
          showExplanation={showExplanation}
        />
      </View>

      {/* Navigation Controls */}
      <View style={styles.navigationContainer}>
        <TouchableOpacity 
          style={[
            styles.navButton, 
            styles.prevButton,
            currentExerciseIndex === 0 && styles.disabledButton
          ]}
          onPress={goToPreviousExercise}
          disabled={currentExerciseIndex === 0}
        >
          <Text style={[
            styles.navButtonText,
            currentExerciseIndex === 0 && styles.disabledButtonText
          ]}>
            ← Previous
          </Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[
            styles.navButton, 
            styles.nextButton,
            !canGoNext && styles.disabledButton
          ]}
          onPress={() => {
            console.log('Next/Finish button pressed', { currentExerciseIndex, exercisesLength: exercises.length, canGoNext });
            if (canGoNext) {
              goToNextExercise();
            }
          }}
          disabled={!canGoNext}
        >
          <Text style={[
            styles.navButtonText,
            !canGoNext && styles.disabledButtonText
          ]}>
            {currentExerciseIndex === exercises.length - 1 ? 'Finish' : 'Next →'}
          </Text>
        </TouchableOpacity>
      </View>

      <View style={styles.progressBar}>
        <View 
          style={[
            styles.progressFill, 
            { width: `${((currentExerciseIndex + 1) / exercises.length) * 100}%` }
          ]} 
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f7fa',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f7fa',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f7fa',
    paddingHorizontal: 20,
  },
  emptyText: {
    fontSize: 18,
    color: '#666',
    textAlign: 'center',
    marginBottom: 20,
  },
  backButton: {
    backgroundColor: '#2E8B57',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
  },
  backButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
  header: {
    backgroundColor: '#2E8B57',
    paddingTop: 60,
    paddingBottom: 20,
    paddingHorizontal: 20,
  },
  headerBackButton: {
    marginBottom: 16,
  },
  headerBackButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 4,
  },
  arabicTitle: {
    fontSize: 18,
    color: '#e8f5e8',
    fontFamily: 'serif',
    marginBottom: 12,
    textAlign: 'right',
  },
  progressContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  progressText: {
    color: '#e8f5e8',
    fontSize: 14,
  },
  scoreText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '600',
  },
  exerciseContainer: {
    flex: 1,
    paddingTop: 10,
  },
  progressBar: {
    height: 4,
    backgroundColor: '#e0e0e0',
    marginHorizontal: 16,
    marginBottom: 20,
    borderRadius: 2,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#2E8B57',
    borderRadius: 2,
  },
  navigationContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 10,
    backgroundColor: '#ffffff',
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  navButton: {
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    minWidth: 100,
    alignItems: 'center',
  },
  prevButton: {
    backgroundColor: '#f0f0f0',
  },
  nextButton: {
    backgroundColor: '#2E8B57',
  },
  disabledButton: {
    backgroundColor: '#e0e0e0',
  },
  navButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  disabledButtonText: {
    color: '#999',
  },
});

export default ExercisesScreen;
