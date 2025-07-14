import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert } from 'react-native';

const IrabAnalysisExercise = ({ exercise, onAnswer, showExplanation }) => {
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [wordAnswers, setWordAnswers] = useState({});
  const [isCompleted, setIsCompleted] = useState(false);

  // Parse the sentence and questions from the exercise data
  const parseExerciseData = () => {
    try {
      const data = JSON.parse(exercise.correct_answer);
      return {
        sentence: data.sentence,
        words: data.words
      };
    } catch (error) {
      console.error('Error parsing exercise data:', error);
      return {
        sentence: '',
        words: []
      };
    }
  };

  const { sentence, words } = parseExerciseData();

  // Reset states when exercise changes
  useEffect(() => {
    setCurrentWordIndex(0);
    setCurrentQuestionIndex(0);
    setSelectedOption(null);
    setIsAnswered(false);
    setWordAnswers({});
    setIsCompleted(false);
  }, [exercise.id]);

  const currentWord = words[currentWordIndex];
  const currentQuestion = currentWord?.questions?.[currentQuestionIndex];

  const handleSubmitAnswer = () => {
    if (!selectedOption) {
      Alert.alert('خطأ', 'يرجى اختيار إجابة');
      return;
    }

    const wordKey = `word_${currentWordIndex}`;
    const questionKey = `question_${currentQuestionIndex}`;
    
    // Store the answer
    setWordAnswers(prev => ({
      ...prev,
      [wordKey]: {
        ...prev[wordKey],
        [questionKey]: {
          answer: selectedOption,
          isCorrect: selectedOption === currentQuestion.correct_answer
        }
      }
    }));

    setIsAnswered(true);

    // Move to next question after a short delay
    setTimeout(() => {
      moveToNextQuestion();
    }, 1500);
  };

  const moveToNextQuestion = () => {
    const totalQuestionsForCurrentWord = currentWord?.questions?.length || 0;
    
    if (currentQuestionIndex < totalQuestionsForCurrentWord - 1) {
      // Move to next question for the same word
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else if (currentWordIndex < words.length - 1) {
      // Move to next word, reset to first question
      setCurrentWordIndex(currentWordIndex + 1);
      setCurrentQuestionIndex(0);
    } else {
      // Exercise completed
      setIsCompleted(true);
      calculateAndSubmitScore();
    }

    setSelectedOption(null);
    setIsAnswered(false);
  };

  const calculateProgress = () => {
    let totalQuestions = 0;
    let completedQuestions = 0;
    
    words.forEach((word, wordIdx) => {
      const questionsInWord = word.questions?.length || 0;
      totalQuestions += questionsInWord;
      
      if (wordIdx < currentWordIndex) {
        // All questions in previous words are completed
        completedQuestions += questionsInWord;
      } else if (wordIdx === currentWordIndex) {
        // Add completed questions in current word
        completedQuestions += currentQuestionIndex + (isAnswered ? 1 : 0);
      }
    });
    
    return totalQuestions > 0 ? (completedQuestions / totalQuestions) * 100 : 0;
  };

  const calculateAndSubmitScore = () => {
    let totalQuestions = 0;
    let correctAnswers = 0;

    // Calculate total questions across all words
    words.forEach(word => {
      totalQuestions += word.questions?.length || 0;
    });

    // Count correct answers
    Object.values(wordAnswers).forEach(wordAnswers => {
      Object.values(wordAnswers).forEach(questionAnswer => {
        if (questionAnswer.isCorrect) {
          correctAnswers++;
        }
      });
    });

    // Add the current answer if it's correct
    if (selectedOption === currentQuestion?.correct_answer) {
      correctAnswers++;
    }

    const score = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0;
    
    // Submit the final answer to parent component
    onAnswer(`تم إكمال التحليل النحوي بنجاح - النتيجة: ${score}%`);
  };

  if (isCompleted) {
    return (
      <View style={styles.completedContainer}>
        <Text style={styles.completedTitle}>🎉 تم إكمال التحليل النحوي!</Text>
        <Text style={styles.completedText}>
          لقد أكملت تحليل جميع كلمات الجملة بنجاح
        </Text>
        <Text style={styles.sentenceText}>{sentence}</Text>
      </View>
    );
  }

  if (!currentWord || !currentQuestion) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>خطأ في تحميل التمرين</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.instructionText}>حلل الجملة التالية نحوياً:</Text>
      <Text style={styles.sentenceText}>{sentence}</Text>
      
      <View style={styles.progressContainer}>
        <Text style={styles.progressText}>
          الكلمة {currentWordIndex + 1} من {words.length} - السؤال {currentQuestionIndex + 1} من {currentWord?.questions?.length || 0}
        </Text>
        <View style={styles.progressBar}>
          <View 
            style={[
              styles.progressFill, 
              { 
                width: `${calculateProgress()}%` 
              }
            ]} 
          />
        </View>
      </View>

      <View style={styles.currentWordContainer}>
        <Text style={styles.currentWordLabel}>الكلمة الحالية:</Text>
        <Text style={styles.currentWordText}>{currentWord.text}</Text>
      </View>

      <Text style={styles.questionText}>{currentQuestion.question}</Text>
      
      <View style={styles.optionsContainer}>
        {currentQuestion.options?.map((option, index) => (
          <TouchableOpacity
            key={index}
            style={[
              styles.optionButton,
              selectedOption === option && styles.selectedOption,
              showExplanation && isAnswered && option === currentQuestion.correct_answer && styles.correctOption,
              showExplanation && isAnswered && selectedOption === option && option !== currentQuestion.correct_answer && styles.incorrectOption,
            ]}
            onPress={() => !isAnswered && setSelectedOption(option)}
            disabled={isAnswered}
          >
            <Text style={[
              styles.optionText,
              selectedOption === option && styles.selectedOptionText,
            ]}>
              {option}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
      
      {!isAnswered && (
        <TouchableOpacity style={styles.submitButton} onPress={handleSubmitAnswer}>
          <Text style={styles.submitButtonText}>إرسال الإجابة</Text>
        </TouchableOpacity>
      )}
      
      {isAnswered && showExplanation && currentQuestion.explanation && (
        <View style={styles.explanationContainer}>
          <Text style={styles.explanationTitle}>الشرح:</Text>
          <Text style={styles.explanationText}>{currentQuestion.explanation}</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  instructionText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2E8B57',
    marginBottom: 12,
    textAlign: 'center',
  },
  sentenceText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'center',
    marginBottom: 16,
    fontFamily: 'serif',
    backgroundColor: '#f8f9fa',
    padding: 12,
    borderRadius: 8,
    borderWidth: 2,
    borderColor: '#2E8B57',
  },
  progressContainer: {
    marginBottom: 16,
  },
  progressText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    marginBottom: 8,
  },
  progressBar: {
    height: 6,
    backgroundColor: '#e0e0e0',
    borderRadius: 3,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#2E8B57',
  },
  currentWordContainer: {
    backgroundColor: '#e8f5e8',
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
    alignItems: 'center',
  },
  currentWordLabel: {
    fontSize: 14,
    color: '#2E8B57',
    fontWeight: '600',
    marginBottom: 4,
  },
  currentWordText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2E8B57',
    fontFamily: 'serif',
  },
  questionText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
    textAlign: 'center',
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
    textAlign: 'center',
    fontFamily: 'serif',
  },
  selectedOptionText: {
    fontWeight: '600',
    color: '#2196F3',
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
  completedContainer: {
    alignItems: 'center',
    padding: 20,
  },
  completedTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2E8B57',
    marginBottom: 12,
    textAlign: 'center',
  },
  completedText: {
    fontSize: 16,
    color: '#333',
    textAlign: 'center',
    marginBottom: 16,
  },
  errorContainer: {
    alignItems: 'center',
    padding: 20,
  },
  errorText: {
    fontSize: 16,
    color: '#f44336',
    textAlign: 'center',
  },
});

export default IrabAnalysisExercise;
