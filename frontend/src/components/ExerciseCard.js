import React from 'react';
import { View, StyleSheet } from 'react-native';
import MultipleChoiceExercise from './MultipleChoiceExercise';
import IrabAnalysisExercise from './IrabAnalysisExercise';

/**
 * ExerciseCard Component
 * 
 * This component has been refactored to use separate components for different exercise types.
 * All exercises are now multiple choice - fill_blank exercises have been converted to 
 * multiple_choice with options in the database.
 * 
 * Previously supported:
 * - multiple_choice: Multiple choice questions with selectable options
 * - fill_blank: Text input exercises (removed - converted to multiple choice)
 * 
 * Currently supported:
 * - multiple_choice: All exercises now use this type with selectable options
 * - irab_analysis: Multi-step grammatical analysis exercises for Arabic sentences
 */

const ExerciseCard = ({ exercise, onAnswer, showExplanation }) => {
  const renderExercise = () => {
    switch (exercise.exercise_type) {
      case 'irab_analysis':
        return (
          <IrabAnalysisExercise 
            exercise={exercise}
            onAnswer={onAnswer}
            showExplanation={showExplanation}
          />
        );
      case 'multiple_choice':
      default:
        return (
          <MultipleChoiceExercise 
            exercise={exercise}
            onAnswer={onAnswer}
            showExplanation={showExplanation}
          />
        );
    }
  };

  return (
    <View style={styles.card}>
      {renderExercise()}
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
