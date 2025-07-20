import React from 'react';
import { View, StyleSheet } from 'react-native';
import IrabAnalysisExercise from './IrabAnalysisExercise';

/**
 * ExerciseCard Component
 * 
 * This component now exclusively handles irab analysis exercises.
 * All lessons have been converted to use comprehensive irab analysis format
 * for deep grammatical understanding of Arabic sentences.
 * 
 * Exercise Type:
 * - irab_analysis: Multi-step grammatical analysis exercises where students
 *   analyze each word in Arabic sentences, identifying word types, grammatical
 *   positions, and inflection cases step by step.
 */

const ExerciseCard = ({ exercise, onAnswer, showExplanation }) => {
  // All exercises are now irab_analysis type
  return (
    <View style={styles.card}>
      <IrabAnalysisExercise 
        exercise={exercise}
        onAnswer={onAnswer}
        showExplanation={showExplanation}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 20,
    marginVertical: 10,
    marginHorizontal: 16,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
});

export default ExerciseCard;
