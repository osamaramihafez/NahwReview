import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { api } from '../../services/api';
import ExerciseForm from './ExerciseForm';

const ExercisesAdmin = () => {
  const [exercises, setExercises] = useState([]);
  const [lessons, setLessons] = useState([]);
  const [levels, setLevels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingExercise, setEditingExercise] = useState(null);
  const [selectedLesson, setSelectedLesson] = useState('all');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [levelsResponse] = await Promise.all([
        api.get('/levels'),
      ]);
      
      setLevels(levelsResponse.data);
      
      // Fetch all lessons and exercises
      const allLessons = [];
      const allExercises = [];
      
      for (const level of levelsResponse.data) {
        try {
          const lessonsResponse = await api.get(`/levels/${level.id}/lessons`);
          const lessonsWithLevel = lessonsResponse.data.map(lesson => ({
            ...lesson,
            level_name: level.name
          }));
          allLessons.push(...lessonsWithLevel);
          
          // Fetch exercises for each lesson
          for (const lesson of lessonsResponse.data) {
            try {
              const exercisesResponse = await api.get(`/lessons/${lesson.id}/exercises`);
              const exercisesWithInfo = exercisesResponse.data.map(exercise => ({
                ...exercise,
                lesson_title: lesson.title,
                level_name: level.name,
                level_id: level.id
              }));
              allExercises.push(...exercisesWithInfo);
            } catch (error) {
              console.warn(`Failed to fetch exercises for lesson ${lesson.id}:`, error);
            }
          }
        } catch (error) {
          console.warn(`Failed to fetch lessons for level ${level.id}:`, error);
        }
      }
      
      setLessons(allLessons);
      setExercises(allExercises);
    } catch (error) {
      console.error('Error fetching data:', error);
      Alert.alert('Error', 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateExercise = () => {
    setEditingExercise(null);
    setShowForm(true);
  };

  const handleEditExercise = (exercise) => {
    setEditingExercise(exercise);
    setShowForm(true);
  };

  const handleFormSubmit = async (exerciseData) => {
    try {
      if (editingExercise) {
        // Update existing exercise
        await api.put(`/exercises/${editingExercise.id}`, exerciseData);
      } else {
        // Create new exercise
        await api.post('/exercises', exerciseData);
      }
      setShowForm(false);
      setEditingExercise(null);
      fetchData();
      Alert.alert('Success', editingExercise ? 'Exercise updated successfully' : 'Exercise created successfully');
    } catch (error) {
      console.error('Error saving exercise:', error);
      Alert.alert('Error', 'Failed to save exercise');
    }
  };

  const handleDeleteExercise = (exerciseId) => {
    Alert.alert(
      'Confirm Delete',
      'Are you sure you want to delete this exercise?',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Delete', 
          style: 'destructive',
          onPress: async () => {
            try {
              await api.delete(`/exercises/${exerciseId}`);
              fetchData();
              Alert.alert('Success', 'Exercise deleted successfully');
            } catch (error) {
              console.error('Error deleting exercise:', error);
              Alert.alert('Error', 'Failed to delete exercise');
            }
          }
        }
      ]
    );
  };

  const filteredExercises = selectedLesson === 'all' 
    ? exercises 
    : exercises.filter(exercise => exercise.lesson_id === parseInt(selectedLesson));

  const getExerciseTypeColor = (type) => {
    switch (type.toLowerCase()) {
      case 'multiple_choice':
        return '#3498db';
      case 'irab_analysis':
        return '#e67e22';
      case 'fill_blank':
        return '#9b59b6';
      default:
        return '#7f8c8d';
    }
  };

  const formatExerciseType = (type) => {
    switch (type.toLowerCase()) {
      case 'multiple_choice':
        return 'Multiple Choice';
      case 'irab_analysis':
        return 'I\'rab Analysis';
      case 'fill_blank':
        return 'Fill in the Blank';
      default:
        return type;
    }
  };

  if (showForm) {
    return (
      <ExerciseForm
        exercise={editingExercise}
        lessons={lessons}
        onSubmit={handleFormSubmit}
        onCancel={() => {
          setShowForm(false);
          setEditingExercise(null);
        }}
      />
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Exercises Management</Text>
        <TouchableOpacity style={styles.addButton} onPress={handleCreateExercise}>
          <Text style={styles.addButtonText}>+ Add Exercise</Text>
        </TouchableOpacity>
      </View>

      {/* Lesson Filter */}
      <View style={styles.filterContainer}>
        <Text style={styles.filterLabel}>Filter by Lesson:</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterScroll}>
          <TouchableOpacity
            style={[styles.filterChip, selectedLesson === 'all' && styles.activeFilter]}
            onPress={() => setSelectedLesson('all')}
          >
            <Text style={[styles.filterText, selectedLesson === 'all' && styles.activeFilterText]}>
              All Lessons
            </Text>
          </TouchableOpacity>
          {lessons.map((lesson) => (
            <TouchableOpacity
              key={lesson.id}
              style={[styles.filterChip, selectedLesson === lesson.id.toString() && styles.activeFilter]}
              onPress={() => setSelectedLesson(lesson.id.toString())}
            >
              <Text style={[styles.filterText, selectedLesson === lesson.id.toString() && styles.activeFilterText]}>
                {lesson.title}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {loading ? (
        <Text style={styles.loadingText}>Loading exercises...</Text>
      ) : (
        <ScrollView style={styles.exercisesList}>
          {filteredExercises.map((exercise) => (
            <View key={exercise.id} style={styles.exerciseCard}>
              <View style={styles.exerciseHeader}>
                <View style={styles.exerciseInfo}>
                  <Text style={styles.exerciseQuestion}>{exercise.question}</Text>
                  {exercise.question_arabic && (
                    <Text style={styles.exerciseArabicQuestion}>{exercise.question_arabic}</Text>
                  )}
                  <View style={styles.exerciseMeta}>
                    <View style={[
                      styles.typeChip, 
                      { backgroundColor: getExerciseTypeColor(exercise.exercise_type) }
                    ]}>
                      <Text style={styles.typeText}>{formatExerciseType(exercise.exercise_type)}</Text>
                    </View>
                    <Text style={styles.metaText}>Order: {exercise.order}</Text>
                  </View>
                  <Text style={styles.lessonInfo}>
                    {exercise.level_name} → {exercise.lesson_title}
                  </Text>
                  <Text style={styles.correctAnswer}>
                    Correct Answer: {exercise.correct_answer}
                  </Text>
                  {exercise.explanation && (
                    <Text style={styles.explanation} numberOfLines={2}>
                      Explanation: {exercise.explanation}
                    </Text>
                  )}
                </View>
                <View style={styles.exerciseActions}>
                  <TouchableOpacity
                    style={styles.editButton}
                    onPress={() => handleEditExercise(exercise)}
                  >
                    <Text style={styles.editButtonText}>Edit</Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    style={styles.deleteButton}
                    onPress={() => handleDeleteExercise(exercise.id)}
                  >
                    <Text style={styles.deleteButtonText}>Delete</Text>
                  </TouchableOpacity>
                </View>
              </View>
              
              {/* Show options for multiple choice exercises */}
              {exercise.exercise_type === 'multiple_choice' && exercise.options && exercise.options.length > 0 && (
                <View style={styles.optionsContainer}>
                  <Text style={styles.optionsTitle}>Options:</Text>
                  {exercise.options.map((option, index) => (
                    <View key={option.id || index} style={styles.optionItem}>
                      <Text style={[
                        styles.optionText,
                        option.is_correct && styles.correctOption
                      ]}>
                        {option.option_text} {option.is_correct && '✓'}
                      </Text>
                    </View>
                  ))}
                </View>
              )}
            </View>
          ))}
          {filteredExercises.length === 0 && (
            <Text style={styles.emptyText}>
              {selectedLesson === 'all' 
                ? 'No exercises found. Create your first exercise!' 
                : 'No exercises found for this lesson.'}
            </Text>
          )}
        </ScrollView>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  addButton: {
    backgroundColor: '#27ae60',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  addButtonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 16,
  },
  filterContainer: {
    marginBottom: 20,
  },
  filterLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2c3e50',
    marginBottom: 10,
  },
  filterScroll: {
    flexDirection: 'row',
  },
  filterChip: {
    backgroundColor: '#ecf0f1',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    marginRight: 10,
  },
  activeFilter: {
    backgroundColor: '#3498db',
  },
  filterText: {
    color: '#7f8c8d',
    fontWeight: '600',
  },
  activeFilterText: {
    color: '#fff',
  },
  loadingText: {
    textAlign: 'center',
    fontSize: 16,
    color: '#7f8c8d',
    marginTop: 50,
  },
  exercisesList: {
    flex: 1,
  },
  exerciseCard: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  exerciseHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 10,
  },
  exerciseInfo: {
    flex: 1,
    marginRight: 15,
  },
  exerciseQuestion: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 5,
  },
  exerciseArabicQuestion: {
    fontSize: 16,
    color: '#34495e',
    marginBottom: 10,
    fontWeight: '600',
  },
  exerciseMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
    gap: 10,
  },
  typeChip: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  typeText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  metaText: {
    fontSize: 12,
    color: '#7f8c8d',
  },
  lessonInfo: {
    fontSize: 14,
    color: '#7f8c8d',
    marginBottom: 5,
  },
  correctAnswer: {
    fontSize: 14,
    color: '#27ae60',
    fontWeight: '600',
    marginBottom: 5,
  },
  explanation: {
    fontSize: 14,
    color: '#34495e',
    fontStyle: 'italic',
  },
  exerciseActions: {
    flexDirection: 'row',
    gap: 10,
  },
  editButton: {
    backgroundColor: '#3498db',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 6,
  },
  editButtonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 14,
  },
  deleteButton: {
    backgroundColor: '#e74c3c',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 6,
  },
  deleteButtonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 14,
  },
  optionsContainer: {
    borderTopWidth: 1,
    borderTopColor: '#ecf0f1',
    paddingTop: 10,
    marginTop: 10,
  },
  optionsTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2c3e50',
    marginBottom: 8,
  },
  optionItem: {
    marginBottom: 4,
  },
  optionText: {
    fontSize: 14,
    color: '#34495e',
    paddingVertical: 2,
  },
  correctOption: {
    color: '#27ae60',
    fontWeight: '600',
  },
  emptyText: {
    textAlign: 'center',
    fontSize: 16,
    color: '#7f8c8d',
    marginTop: 50,
  },
});

export default ExercisesAdmin;
