import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, TextInput, Alert } from 'react-native';

const ExerciseCard = ({ exercise, onAnswer, showExplanation }) => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [fillBlankAnswer, setFillBlankAnswer] = useState('');
  const [isAnswered, setIsAnswered] = useState(false);

  // Reset states when exercise changes
  React.useEffect(() => {
    setSelectedOption(null);
    setFillBlankAnswer('');
    setIsAnswered(false);
  }, [exercise.id]);

  const handleSubmitAnswer = async () => {
    let userAnswer = '';
    
    if (exercise.exercise_type === 'multiple_choice') {
      if (!selectedOption) {
        Alert.alert('Error', 'Please select an option');
        return;
      }
      userAnswer = selectedOption;
    } else if (exercise.exercise_type === 'fill_blank') {
      if (!fillBlankAnswer.trim()) {
        Alert.alert('Error', 'Please enter your answer');
        return;
      }
      userAnswer = fillBlankAnswer.trim();
    }

    setIsAnswered(true);
    onAnswer(userAnswer);
  };

  const renderMultipleChoice = () => (
    <View style={styles.optionsContainer}>
      {exercise.options?.map((option) => (
        <TouchableOpacity
          key={option.id}
          style={[
            styles.optionButton,
            selectedOption === option.option_text && styles.selectedOption,
            showExplanation && option.is_correct && styles.correctOption,
            showExplanation && selectedOption === option.option_text && !option.is_correct && styles.incorrectOption,
          ]}
          onPress={() => !isAnswered && setSelectedOption(option.option_text)}
          disabled={isAnswered}
        >
          <Text style={[
            styles.optionText,
            selectedOption === option.option_text && styles.selectedOptionText,
          ]}>
            {option.option_text}
          </Text>
        </TouchableOpacity>
      ))}
    </View>
  );

  const renderFillBlank = () => (
    <View style={styles.fillBlankContainer}>
      <TextInput
        style={[
          styles.fillBlankInput,
          isAnswered && styles.disabledInput,
        ]}
        value={fillBlankAnswer}
        onChangeText={setFillBlankAnswer}
        placeholder="Enter your answer..."
        editable={!isAnswered}
        textAlign="right" // For Arabic text
      />
      {showExplanation && (
        <Text style={styles.correctAnswer}>
          Correct answer: {exercise.correct_answer}
        </Text>
      )}
    </View>
  );

  return (
    <View style={styles.card}>
      <Text style={styles.questionText}>{exercise.question}</Text>
      {exercise.question_arabic && (
        <Text style={styles.arabicQuestion}>{exercise.question_arabic}</Text>
      )}
      
      {exercise.exercise_type === 'multiple_choice' && renderMultipleChoice()}
      {exercise.exercise_type === 'fill_blank' && renderFillBlank()}
      
      {!isAnswered && (
        <TouchableOpacity style={styles.submitButton} onPress={handleSubmitAnswer}>
          <Text style={styles.submitButtonText}>Submit Answer</Text>
        </TouchableOpacity>
      )}
      
      {isAnswered && showExplanation && exercise.explanation && (
        <View style={styles.explanationContainer}>
          <Text style={styles.explanationTitle}>Explanation:</Text>
          <Text style={styles.explanationText}>{exercise.explanation}</Text>
        </View>
      )}
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
  questionText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
    lineHeight: 24,
  },
  arabicQuestion: {
    fontSize: 16,
    color: '#666',
    marginBottom: 16,
    textAlign: 'right',
    fontFamily: 'serif',
    lineHeight: 22,
  },
  optionsContainer: {
    marginBottom: 16,
  },
  optionButton: {
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    padding: 12,
    marginVertical: 4,
    borderWidth: 1,
    borderColor: '#e9ecef',
  },
  selectedOption: {
    backgroundColor: '#e3f2fd',
    borderColor: '#2196F3',
  },
  correctOption: {
    backgroundColor: '#e8f5e8',
    borderColor: '#4caf50',
  },
  incorrectOption: {
    backgroundColor: '#ffebee',
    borderColor: '#f44336',
  },
  optionText: {
    fontSize: 16,
    color: '#333',
  },
  selectedOptionText: {
    fontWeight: '600',
    color: '#2196F3',
  },
  fillBlankContainer: {
    marginBottom: 16,
  },
  fillBlankInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    backgroundColor: '#f8f9fa',
  },
  disabledInput: {
    backgroundColor: '#e9ecef',
    color: '#666',
  },
  correctAnswer: {
    marginTop: 8,
    fontSize: 14,
    color: '#4caf50',
    fontWeight: '600',
  },
  submitButton: {
    backgroundColor: '#2E8B57',
    borderRadius: 8,
    padding: 14,
    alignItems: 'center',
  },
  submitButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
  explanationContainer: {
    marginTop: 16,
    padding: 12,
    backgroundColor: '#f0f8f0',
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#2E8B57',
  },
  explanationTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2E8B57',
    marginBottom: 4,
  },
  explanationText: {
    fontSize: 14,
    color: '#333',
    lineHeight: 20,
  },
});

export default ExerciseCard;
