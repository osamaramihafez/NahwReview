import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { api } from '../../services/api';
import LessonForm from './LessonForm';

const LessonsAdmin = () => {
  const [lessons, setLessons] = useState([]);
  const [levels, setLevels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingLesson, setEditingLesson] = useState(null);
  const [selectedLevel, setSelectedLevel] = useState('all');

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
      
      // Fetch all lessons from all levels
      const allLessons = [];
      for (const level of levelsResponse.data) {
        try {
          const lessonsResponse = await api.get(`/levels/${level.id}/lessons`);
          const lessonsWithLevel = lessonsResponse.data.map(lesson => ({
            ...lesson,
            level_name: level.name
          }));
          allLessons.push(...lessonsWithLevel);
        } catch (error) {
          console.warn(`Failed to fetch lessons for level ${level.id}:`, error);
        }
      }
      
      setLessons(allLessons);
    } catch (error) {
      console.error('Error fetching data:', error);
      Alert.alert('Error', 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateLesson = () => {
    setEditingLesson(null);
    setShowForm(true);
  };

  const handleEditLesson = (lesson) => {
    setEditingLesson(lesson);
    setShowForm(true);
  };

  const handleFormSubmit = async (lessonData) => {
    try {
      if (editingLesson) {
        // Update existing lesson
        await api.put(`/lessons/${editingLesson.id}`, lessonData);
      } else {
        // Create new lesson
        await api.post('/lessons', lessonData);
      }
      setShowForm(false);
      setEditingLesson(null);
      fetchData();
      Alert.alert('Success', editingLesson ? 'Lesson updated successfully' : 'Lesson created successfully');
    } catch (error) {
      console.error('Error saving lesson:', error);
      Alert.alert('Error', 'Failed to save lesson');
    }
  };

  const handleDeleteLesson = (lessonId) => {
    Alert.alert(
      'Confirm Delete',
      'Are you sure you want to delete this lesson? This will also delete all associated exercises.',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Delete', 
          style: 'destructive',
          onPress: async () => {
            try {
              await api.delete(`/lessons/${lessonId}`);
              fetchData();
              Alert.alert('Success', 'Lesson deleted successfully');
            } catch (error) {
              console.error('Error deleting lesson:', error);
              Alert.alert('Error', 'Failed to delete lesson');
            }
          }
        }
      ]
    );
  };

  const filteredLessons = selectedLevel === 'all' 
    ? lessons 
    : lessons.filter(lesson => lesson.level_id === parseInt(selectedLevel));

  if (showForm) {
    return (
      <LessonForm
        lesson={editingLesson}
        levels={levels}
        onSubmit={handleFormSubmit}
        onCancel={() => {
          setShowForm(false);
          setEditingLesson(null);
        }}
      />
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Lessons Management</Text>
        <TouchableOpacity style={styles.addButton} onPress={handleCreateLesson}>
          <Text style={styles.addButtonText}>+ Add Lesson</Text>
        </TouchableOpacity>
      </View>

      {/* Level Filter */}
      <View style={styles.filterContainer}>
        <Text style={styles.filterLabel}>Filter by Level:</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterScroll}>
          <TouchableOpacity
            style={[styles.filterChip, selectedLevel === 'all' && styles.activeFilter]}
            onPress={() => setSelectedLevel('all')}
          >
            <Text style={[styles.filterText, selectedLevel === 'all' && styles.activeFilterText]}>
              All Levels
            </Text>
          </TouchableOpacity>
          {levels.map((level) => (
            <TouchableOpacity
              key={level.id}
              style={[styles.filterChip, selectedLevel === level.id.toString() && styles.activeFilter]}
              onPress={() => setSelectedLevel(level.id.toString())}
            >
              <Text style={[styles.filterText, selectedLevel === level.id.toString() && styles.activeFilterText]}>
                {level.name}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {loading ? (
        <Text style={styles.loadingText}>Loading lessons...</Text>
      ) : (
        <ScrollView style={styles.lessonsList}>
          {filteredLessons.map((lesson) => (
            <View key={lesson.id} style={styles.lessonCard}>
              <View style={styles.lessonHeader}>
                <View style={styles.lessonInfo}>
                  <Text style={styles.lessonTitle}>{lesson.title}</Text>
                  {lesson.arabic_title && (
                    <Text style={styles.lessonArabicTitle}>{lesson.arabic_title}</Text>
                  )}
                  <Text style={styles.lessonLevel}>Level: {lesson.level_name}</Text>
                  <Text style={styles.lessonOrder}>Order: {lesson.order}</Text>
                  {lesson.description && (
                    <Text style={styles.lessonDescription}>{lesson.description}</Text>
                  )}
                </View>
                <View style={styles.lessonActions}>
                  <TouchableOpacity
                    style={styles.editButton}
                    onPress={() => handleEditLesson(lesson)}
                  >
                    <Text style={styles.editButtonText}>Edit</Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    style={styles.deleteButton}
                    onPress={() => handleDeleteLesson(lesson.id)}
                  >
                    <Text style={styles.deleteButtonText}>Delete</Text>
                  </TouchableOpacity>
                </View>
              </View>
              <View style={styles.lessonStats}>
                <Text style={styles.statsText}>
                  Exercises: {lesson.exercises ? lesson.exercises.length : 0}
                </Text>
              </View>
            </View>
          ))}
          {filteredLessons.length === 0 && (
            <Text style={styles.emptyText}>
              {selectedLevel === 'all' 
                ? 'No lessons found. Create your first lesson!' 
                : 'No lessons found for this level.'}
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
  lessonsList: {
    flex: 1,
  },
  lessonCard: {
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
  lessonHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 10,
  },
  lessonInfo: {
    flex: 1,
    marginRight: 15,
  },
  lessonTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 5,
  },
  lessonArabicTitle: {
    fontSize: 16,
    color: '#34495e',
    marginBottom: 5,
    fontWeight: '600',
  },
  lessonLevel: {
    fontSize: 14,
    color: '#7f8c8d',
    marginBottom: 2,
  },
  lessonOrder: {
    fontSize: 14,
    color: '#7f8c8d',
    marginBottom: 5,
  },
  lessonDescription: {
    fontSize: 14,
    color: '#34495e',
  },
  lessonActions: {
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
  lessonStats: {
    borderTopWidth: 1,
    borderTopColor: '#ecf0f1',
    paddingTop: 10,
  },
  statsText: {
    fontSize: 14,
    color: '#7f8c8d',
  },
  emptyText: {
    textAlign: 'center',
    fontSize: 16,
    color: '#7f8c8d',
    marginTop: 50,
  },
});

export default LessonsAdmin;
