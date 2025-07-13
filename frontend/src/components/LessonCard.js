import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

const LessonCard = ({ lesson, onPress, isCompleted = false }) => {
  return (
    <TouchableOpacity style={[styles.card, isCompleted && styles.completedCard]} onPress={onPress}>
      <View style={styles.cardContent}>
        <View style={styles.lessonHeader}>
          <Text style={styles.lessonOrder}>Lesson {lesson.order}</Text>
          {isCompleted && <Text style={styles.completedBadge}>✓</Text>}
        </View>
        <Text style={styles.lessonTitle}>{lesson.title}</Text>
        {lesson.arabic_title && (
          <Text style={styles.arabicTitle}>{lesson.arabic_title}</Text>
        )}
        <Text style={styles.lessonDescription}>{lesson.description}</Text>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 10,
    padding: 16,
    marginVertical: 6,
    marginHorizontal: 16,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  completedCard: {
    backgroundColor: '#f0f8f0',
    borderLeftWidth: 4,
    borderLeftColor: '#2E8B57',
  },
  cardContent: {
    flex: 1,
  },
  lessonHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  lessonOrder: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2E8B57',
  },
  completedBadge: {
    fontSize: 18,
    color: '#2E8B57',
    fontWeight: 'bold',
  },
  lessonTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  arabicTitle: {
    fontSize: 16,
    color: '#666',
    marginBottom: 8,
    textAlign: 'right',
    fontFamily: 'serif',
  },
  lessonDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 18,
  },
});

export default LessonCard;
