import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert, ScrollView } from 'react-native';

/**
 * IrabAnalysisExercise Component
 * 
 * This component handles Arabic grammatical analysis (I'rab) exercises where users
 * analyze each word in a sentence by answering multiple questions about each word's
 * grammatical properties (case, type, function, etc.)
 * 
 * @param {Object} exercise - The exercise data containing the sentence and questions
 * @param {Function} onAnswer - Callback function called when exercise is completed
 * @param {boolean} showExplanation - Whether to show explanations after answers
 */
const IrabAnalysisExercise = ({ exercise, onAnswer, showExplanation }) => {
  // State to track which word we're currently analyzing (0-indexed)
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  
  // State to track which question about the current word we're on (0-indexed)
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  
  // State to store the user's currently selected answer option
  const [selectedOption, setSelectedOption] = useState(null);
  
  // State to track if the current question has been answered
  const [isAnswered, setIsAnswered] = useState(false);
  
  // State to store all answers for all words and questions
  // Structure: { word_0: { question_0: {...}, question_1: {...} }, word_1: {...} }
  const [wordAnswers, setWordAnswers] = useState({});
  
  // State to track if the entire exercise is completed
  const [isCompleted, setIsCompleted] = useState(false);

  // State to store shuffled option indices for each question
  const [shuffledIndices, setShuffledIndices] = useState({});

  /**
   * Fisher-Yates shuffle algorithm to randomize array indices
   */
  const shuffleArray = (array) => {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  };

  /**
   * Get or create shuffled indices for current question
   */
  const getShuffledIndices = () => {
    // Safety check to ensure currentWord and currentQuestion exist
    if (!currentQuestion) return [];
    
    const questionKey = `${currentWordIndex}_${currentQuestionIndex}`;
    
    if (!shuffledIndices[questionKey]) {
      const optionsArray = currentQuestion.options_arabic || currentQuestion.options || [];
      if (optionsArray.length === 0) return [];
      
      const indices = Array.from({ length: optionsArray.length }, (_, i) => i);
      const shuffled = shuffleArray(indices);
      
      setShuffledIndices(prev => ({
        ...prev,
        [questionKey]: shuffled
      }));
      
      return shuffled;
    }
    
    return shuffledIndices[questionKey];
  };

  /**
   * Parse the exercise data from JSON format
   * The exercise.correct_answer contains a JSON string with:
   * - sentence: The Arabic sentence to analyze
   * - sentence_translation: English translation of the sentence
   * - words: Array of words, each with questions about grammatical analysis
   */
  const parseExerciseData = () => {
    try {
      const data = JSON.parse(exercise.correct_answer);
      return {
        sentence: data.sentence,
        sentenceTranslation: data.sentence_translation || '',
        words: data.words || []
      };
    } catch (error) {
      console.error('Error parsing exercise data:', error);
      return {
        sentence: '',
        sentenceTranslation: '',
        words: []
      };
    }
  };

  // Extract the parsed data
  const { sentence, sentenceTranslation, words } = parseExerciseData();

  // Reset all states when the exercise changes (different exercise ID)
  // This ensures we start fresh for each new exercise
  useEffect(() => {
    setCurrentWordIndex(0);
    setCurrentQuestionIndex(0);
    setSelectedOption(null);
    setIsAnswered(false);
    setWordAnswers({});
    setIsCompleted(false);
    setShuffledIndices({}); // Reset shuffled indices for new exercise
  }, [exercise.id]);

  // Get the current word and question objects based on current indices
  const currentWord = words[currentWordIndex];
  const currentQuestion = currentWord?.questions?.[currentQuestionIndex];

  /**
   * Handle submitting an answer for the current question
   * Validates the answer, stores it, and automatically moves to next question
   */
  const handleSubmitAnswer = () => {
    // Validation: ensure user has selected an option
    if (!selectedOption) {
      Alert.alert('خطأ', 'يرجى اختيار إجابة');
      return;
    }

    // Create unique keys for storing this answer
    const wordKey = `word_${currentWordIndex}`;
    const questionKey = `question_${currentQuestionIndex}`;
    
    // Handle both old format (with /) and new format (separate Arabic/English fields)
    // This provides backward compatibility with different data formats
    const correctAnswer = currentQuestion.correct_answer_arabic 
      ? currentQuestion.correct_answer_arabic 
      : currentQuestion.correct_answer;
    
    // Check if the selected answer is correct
    const isCorrect = selectedOption === correctAnswer;
    
    // Store the answer in our state structure
    setWordAnswers(prev => ({
      ...prev,
      [wordKey]: {
        ...prev[wordKey],
        [questionKey]: {
          question: currentQuestion.question,
          selectedAnswer: selectedOption,
          correctAnswer: correctAnswer,
          isCorrect
        }
      }
    }));

    // Mark this question as answered
    setIsAnswered(true);
    
    // Brief delay before moving to next question for better UX
    setTimeout(moveToNextQuestion, 1500);
  };

  /**
   * Navigate to the next question or word in the exercise
   * Logic: First complete all questions for current word, then move to next word
   */
  const moveToNextQuestion = () => {
    // Reset answer-related states for the next question
    setSelectedOption(null);
    setIsAnswered(false);

    // Check if there are more questions for the current word
    if (currentQuestionIndex < (currentWord?.questions?.length || 0) - 1) {
      // Move to next question within the same word
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } 
    // Check if there are more words to analyze
    else if (currentWordIndex < words.length - 1) {
      // Move to the first question of the next word
      setCurrentWordIndex(currentWordIndex + 1);
      setCurrentQuestionIndex(0);
    } 
    // All questions for all words completed
    else {
      setIsCompleted(true);
      calculateAndSubmitScore();
    }
  };

  /**
   * Calculate the overall progress percentage for the progress bar
   * Takes into account all questions across all words
   */
  const calculateProgress = () => {
    let totalQuestions = 0;
    let completedQuestions = 0;
    
    // Count total questions and completed questions
    words.forEach((word, wordIdx) => {
      const questionsInWord = word.questions?.length || 0;
      totalQuestions += questionsInWord;
      
      if (wordIdx < currentWordIndex) {
        // All questions in previous words are completed
        completedQuestions += questionsInWord;
      } else if (wordIdx === currentWordIndex) {
        // Add completed questions in current word + current question if answered
        completedQuestions += currentQuestionIndex + (isAnswered ? 1 : 0);
      }
    });
    
    return totalQuestions > 0 ? (completedQuestions / totalQuestions) * 100 : 0;
  };

  /**
   * Calculate progress segments with correctness information
   * Returns array of segments with their completion status and correctness
   */
  const calculateProgressSegments = () => {
    const segments = [];
    let questionIndex = 0;
    
    words.forEach((word, wordIdx) => {
      const questionsInWord = word.questions?.length || 0;
      
      for (let qIdx = 0; qIdx < questionsInWord; qIdx++) {
        const wordKey = `word_${wordIdx}`;
        const questionKey = `question_${qIdx}`;
        const answer = wordAnswers[wordKey]?.[questionKey];
        
        let status = 'incomplete'; // 'incomplete', 'correct', 'incorrect'
        
        if (wordIdx < currentWordIndex) {
          // Past questions - check if answered correctly
          status = answer?.isCorrect ? 'correct' : 'incorrect';
        } else if (wordIdx === currentWordIndex && qIdx < currentQuestionIndex) {
          // Past questions in current word
          status = answer?.isCorrect ? 'correct' : 'incorrect';
        } else if (wordIdx === currentWordIndex && qIdx === currentQuestionIndex && isAnswered) {
          // Current question that was just answered
          status = answer?.isCorrect ? 'correct' : 'incorrect';
        }
        
        segments.push({
          index: questionIndex,
          status: status,
          width: (1 / words.reduce((total, w) => total + (w.questions?.length || 0), 0)) * 100
        });
        
        questionIndex++;
      }
    });
    
    return segments;
  };

  /**
   * Calculate the final score based on correct answers
   * Returns an object with score details
   */
  const calculateFinalScore = () => {
    let totalQuestions = 0;
    let correctAnswers = 0;

    // Calculate total questions across all words
    words.forEach(word => {
      totalQuestions += word.questions?.length || 0;
    });

    // Count correct answers from stored answers
    Object.values(wordAnswers).forEach(wordAnswers => {
      Object.values(wordAnswers).forEach(questionAnswer => {
        if (questionAnswer.isCorrect) {
          correctAnswers++;
        }
      });
    });

    const score = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0;
    
    return {
      score,
      correctAnswers,
      totalQuestions
    };
  };

  /**
   * Calculate final score and submit results to parent component
   * Called when all questions have been completed
   */
  const calculateAndSubmitScore = () => {
    const { score } = calculateFinalScore();
    
    // Submit the final result to parent component
    try {
      onAnswer(`Irab analysis completed successfully - Score: ${score}%`);
    } catch (error) {
      console.error('Error submitting score:', error);
    }
  };

  // Render completion screen when all questions are done
  if (isCompleted) {
    const { score, correctAnswers, totalQuestions } = calculateFinalScore();
    
    return (
      <ScrollView 
        style={styles.completedContainer} 
        contentContainerStyle={styles.completedContentContainer}
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.completedTitle}>Irab Analysis Completed!</Text>
        
        {/* Display the final score */}
        <View style={styles.scoreContainer}>
          <Text style={styles.scoreText}>Final Score: {score}%</Text>
          <Text style={styles.scoreDetails}>
            {correctAnswers} out of {totalQuestions} questions correct
          </Text>
        </View>
        
        {/* Performance message based on score */}
        <Text style={[
          styles.performanceText,
          { color: score >= 80 ? '#4caf50' : score >= 60 ? '#ff9800' : '#f44336' }
        ]}>
          {score >= 80 ? 'Excellent work! 🌟' : 
           score >= 60 ? 'Good effort! Keep practicing! 👍' : 
           'Keep studying and try again! 📚'}
        </Text>
        
        {sentence && (
          <View style={styles.sentenceContainer}>
            <Text style={styles.sentenceTextArabic}>{sentence}</Text>
            {sentenceTranslation && <Text style={styles.sentenceTextEnglish}>"{sentenceTranslation}"</Text>}
          </View>
        )}
      </ScrollView>
    );
  }

  // Render error screen if data is malformed or missing
  if (!currentWord || !currentQuestion) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>خطأ في تحميل التمرين</Text>
        <Text style={styles.errorDetails}>
          Words: {words.length}, Current Word: {currentWordIndex}, Current Question: {currentQuestionIndex}
        </Text>
      </View>
    );
  }

  // Main exercise interface - render the current question
  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Exercise instructions in English and Arabic */}
      <Text style={styles.instructionText}>
        {exercise.question}
      </Text>

      {/* Compact progress indicator */}
      <View style={styles.progressContainer}>
        <View style={styles.progressBar}>
          {calculateProgressSegments().map((segment, index) => (
            <View
              key={index}
              style={[
                styles.progressSegment,
                {
                  width: `${segment.width}%`,
                  backgroundColor: 
                    segment.status === 'correct' ? '#4caf50' :  // Green for correct
                    segment.status === 'incorrect' ? '#f44336' : // Red for incorrect
                    '#e0e0e0' // Gray for incomplete
                }
              ]}
            />
          ))}
        </View>
      </View>
      
      {/* Display the full sentence with highlighted current word */}
      <View style={styles.sentenceContainer}>
        <Text style={styles.sentenceTextArabic}>
          {words.map((word, index) => (
            <Text
              key={index}
              style={[
                styles.wordText,
                index === currentWordIndex && styles.highlightedWord
              ]}
            >
              {word.text}{index < words.length - 1 ? ' ' : ''}
            </Text>
          ))}
        </Text>
        {sentenceTranslation && <Text style={styles.sentenceTextEnglish}>{sentenceTranslation}</Text>}
      </View>

      {/* Display the current question about the word */}
      <View style={styles.questionContainer}>
        <Text style={styles.questionTextEnglish}>{currentQuestion.question}</Text>
      </View>
      
      {/* Render answer options horizontally */}
      <View style={styles.optionsContainer}>
        {(() => {
          // Safety checks to prevent crashes
          if (!currentQuestion) return null;
          
          const optionsArray = currentQuestion.options_arabic || currentQuestion.options || [];
          if (optionsArray.length === 0) return null;
          
          const shuffledOptionIndices = getShuffledIndices();
          if (shuffledOptionIndices.length === 0) return null;
          
          return shuffledOptionIndices.map((originalIndex, displayIndex) => {
            // Handle both bilingual (Arabic + English) and single language options
            const englishOption = currentQuestion.options ? currentQuestion.options[originalIndex] : optionsArray[originalIndex];
            const arabicOption = currentQuestion.options_arabic ? currentQuestion.options_arabic[originalIndex] : optionsArray[originalIndex];
            const displayOption = currentQuestion.options_arabic ? arabicOption : optionsArray[originalIndex];
            
            // Safety check for undefined options
            if (!displayOption) return null;
            
            return (
              <TouchableOpacity
                key={displayIndex}
                style={[
                  styles.optionButton,
                  // Highlight selected option
                  selectedOption === displayOption && styles.selectedOption,
                  // Show correct answer in green when explanation is enabled and question is answered
                  showExplanation && isAnswered && displayOption === (currentQuestion.correct_answer_arabic || currentQuestion.correct_answer) && styles.correctOption,
                  // Show incorrect selection in red when explanation is enabled
                  showExplanation && isAnswered && selectedOption === displayOption && displayOption !== (currentQuestion.correct_answer_arabic || currentQuestion.correct_answer) && styles.incorrectOption,
                ]}
                onPress={() => !isAnswered && setSelectedOption(displayOption)}
                disabled={isAnswered} // Disable selection after answering
              >
                {/* Render bilingual options or single language option */}
                {currentQuestion.options_arabic ? (
                  <View style={styles.optionTextContainer}>
                    <Text style={[styles.optionTextArabic, selectedOption === displayOption && styles.selectedOptionText]}>
                      {arabicOption}
                    </Text>
                    <Text style={[styles.optionTextEnglish, selectedOption === displayOption && styles.selectedOptionText]}>
                      {englishOption}
                    </Text>
                  </View>
                ) : (
                  <Text style={[styles.optionText, selectedOption === displayOption && styles.selectedOptionText]}>
                    {displayOption}
                  </Text>
                )}
              </TouchableOpacity>
            );
          }).filter(Boolean); // Remove any null elements
        })()}
      </View>

      {/* Submit button - only show when question hasn't been answered yet */}
      {!isAnswered && (
        <TouchableOpacity style={styles.submitButton} onPress={handleSubmitAnswer}>
          <Text style={styles.submitButtonText}>Submit Answer</Text>
        </TouchableOpacity>
      )}
      
      {/* Show explanation after answering (if available and enabled) */}
      {isAnswered && showExplanation && (currentQuestion.explanation || currentQuestion.explanation_arabic) && (
        <View style={styles.explanationContainer}>
          <Text style={styles.explanationTitle}>الشرح:</Text>
          {currentQuestion.explanation_arabic && (
            <Text style={styles.explanationTextArabic}>{currentQuestion.explanation_arabic}</Text>
          )}
          {currentQuestion.explanation && (
            <Text style={styles.explanationTextEnglish}>{currentQuestion.explanation}</Text>
          )}
        </View>
      )}
    </ScrollView>
  );
};

/**
 * StyleSheet for the IrabAnalysisExercise component
 * Organized by UI sections: container, instructions, sentence display, 
 * progress indicators, word highlighting, questions, options, buttons, and explanations
 */
const styles = StyleSheet.create({
  // Main container
  container: {
    flex: 1,
    paddingBottom: 2,
  },
  
  // Exercise instruction styles
  instructionText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2E8B57', // Green theme color
    marginBottom: 4,
    textAlign: 'center',
  },
  instructionTextArabic: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2E8B57',
    marginBottom: 12,
    textAlign: 'center',
    fontFamily: 'serif', // Better for Arabic text
  },
  
  // Sentence display container
  sentenceContainer: {
    marginBottom: 16,
    backgroundColor: '#f8f9fa',
    padding: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#e9ecef',
  },
  sentenceTextArabic: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'center',
    fontFamily: 'serif',
    marginBottom: 8,
    lineHeight: 32, // Better spacing for inline words
  },
  // Individual word styling for inline highlighting
  wordText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    fontFamily: 'serif',
  },
  highlightedWord: {
    backgroundColor: '#d9ffcdff', // Yellow highlight for current word
    paddingHorizontal: 4,
    paddingVertical: 2,
    borderRadius: 4,
    color: '#1d1ac5ff', // Darker text for highlighted word
  },
  sentenceTextEnglish: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    fontStyle: 'italic',
    marginBottom: 8,
  },
  // Translation for current word
  currentWordTranslation: {
    fontSize: 14,
    color: '#856404',
    textAlign: 'center',
    fontStyle: 'italic',
    fontWeight: '500',
  },
  
  // Progress indicator styles
  progressContainer: {
    marginBottom: 16,
  },
  progressText: {
    fontSize: 12,
    color: '#666',
    marginBottom: 6,
    textAlign: 'center',
    fontWeight: '500',
  },
  progressBar: {
    height: 6,
    backgroundColor: '#e0e0e0', // Light gray background
    borderRadius: 3,
    flexDirection: 'row',
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#2E8B57', // Green fill to match theme
    borderRadius: 2,
  },
  progressSegment: {
    height: '100%',
    marginRight: 1,
  },
  
  // Question display styles
  questionContainer: {
    marginBottom: 16,
    backgroundColor: '#e3f2fd', // Light blue background
    padding: 5,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#2196F3', // Blue left border accent
  },
  questionTextArabic: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    textAlign: 'center', // Center Arabic text
    fontFamily: 'serif',
  },
  questionTextEnglish: {
    fontSize: 14,
    color: '#555',
    textAlign: 'center', // Center English text
    marginBottom: 4,
  },
  
  // Answer options styles - horizontal layout
  optionsContainer: {
    marginBottom: 16,
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    gap: 2,
    // justifyContent: 'space-between',
  },
  optionButton: {
    backgroundColor: '#ffffff',
    borderWidth: 2,
    borderColor: '#e0e0e0', // Default gray border
    borderRadius: 8,
    padding: 8,
    marginBottom: 8,
    minWidth: '20%', // Two options per row on smaller screens
    alignItems: 'center',
  },
  selectedOption: {
    backgroundColor: '#e3f2fd', // Light blue when selected
    borderColor: '#2196F3', // Blue border when selected
  },
  correctOption: {
    backgroundColor: '#e8f5e8', // Light green for correct answers
    borderColor: '#4caf50', // Green border
  },
  incorrectOption: {
    backgroundColor: '#ffebee', // Light red for incorrect answers
    borderColor: '#f44336', // Red border
  },
  
  // Option text styles - compact for horizontal layout
  optionTextContainer: {
    alignItems: 'center',
  },
  optionText: {
    fontSize: 14,
    color: '#333',
    textAlign: 'center',
    fontFamily: 'serif',
  },
  optionTextArabic: {
    fontSize: 14,
    color: '#333',
    textAlign: 'center',
    fontFamily: 'serif',
    fontWeight: '600',
    marginBottom: 2,
  },
  optionTextEnglish: {
    fontSize: 11,
    color: '#666',
    textAlign: 'center',
    fontStyle: 'italic',
  },
  selectedOptionText: {
    fontWeight: '600',
    color: '#2196F3', // Blue text for selected option
  },
  
  // Submit button styles
  submitButton: {
    backgroundColor: '#2E8B57', // Green background
    borderRadius: 8,
    padding: 14,
    alignItems: 'center',
  },
  submitButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
  
  // Explanation section styles
  explanationContainer: {
    marginTop: 16,
    padding: 12,
    backgroundColor: '#f0f8f0', // Light green background
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#2E8B57', // Green left border
  },
  explanationTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2E8B57',
    marginBottom: 8,
  },
  explanationText: {
    fontSize: 14,
    color: '#333',
    lineHeight: 20,
  },
  explanationTextArabic: {
    fontSize: 14,
    color: '#333',
    lineHeight: 20,
    fontFamily: 'serif',
    textAlign: 'right', // RTL for Arabic
    marginBottom: 8,
  },
  explanationTextEnglish: {
    fontSize: 14,
    color: '#555',
    lineHeight: 20,
    fontStyle: 'italic',
  },
  
  // Completion screen styles
  completedContainer: {
    flex: 1,
    padding: 20,
  },
  completedContentContainer: {
    alignItems: 'center',
    paddingBottom: 20,
  },
  completedTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2E8B57',
    marginBottom: 16,
    textAlign: 'center',
  },
  completedText: {
    fontSize: 16,
    color: '#333',
    textAlign: 'center',
    marginBottom: 16,
  },
  
  // Score display styles
  scoreContainer: {
    backgroundColor: '#f8f9fa',
    padding: 16,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#2E8B57',
    marginBottom: 16,
    alignItems: 'center',
    minWidth: 200,
  },
  scoreText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2E8B57',
    marginBottom: 4,
  },
  scoreDetails: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
  },
  performanceText: {
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
    marginBottom: 20,
  },
  
  // Error screen styles
  errorContainer: {
    alignItems: 'center',
    padding: 20,
  },
  errorText: {
    fontSize: 16,
    color: '#f44336', // Red for errors
    textAlign: 'center',
    marginBottom: 8,
  },
  errorDetails: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
  },
});

export default IrabAnalysisExercise;
