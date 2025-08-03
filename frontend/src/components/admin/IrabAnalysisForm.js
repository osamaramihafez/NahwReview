import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, TextInput, Alert } from 'react-native';

const IrabAnalysisForm = ({ onSubmit, onCancel, initialData = null, hideButtons = false, onValidate }) => {
  const [sentence, setSentence] = useState(initialData?.sentence || '');
  const [words, setWords] = useState(initialData?.words || []);
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  // Initialize with empty word if no words exist
  const ensureWordsExist = () => {
    if (words.length === 0) {
      setWords([{ text: '', position: 0, questions: [] }]);
    }
  };

  React.useEffect(() => {
    ensureWordsExist();
    // Expose validation function to parent
    if (onValidate) {
      onValidate(handleSubmit);
    }
  }, [onValidate]);

  const addWord = () => {
    const newWord = {
      text: '',
      position: words.length,
      questions: []
    };
    setWords([...words, newWord]);
    setCurrentWordIndex(words.length);
    setCurrentQuestionIndex(0);
  };

  const removeWord = (index) => {
    if (words.length <= 1) {
      Alert.alert('Error', 'At least one word is required');
      return;
    }
    const newWords = words.filter((_, i) => i !== index);
    // Update positions
    const updatedWords = newWords.map((word, i) => ({ ...word, position: i }));
    setWords(updatedWords);
    
    // Adjust current indices
    if (currentWordIndex >= updatedWords.length) {
      setCurrentWordIndex(updatedWords.length - 1);
    }
    setCurrentQuestionIndex(0);
  };

  const updateWordText = (index, text) => {
    const newWords = [...words];
    newWords[index].text = text;
    setWords(newWords);
  };

  const addQuestion = () => {
    if (currentWordIndex >= words.length) return;
    
    const newQuestion = {
      question: '',
      question_arabic: '',
      options: ['', '', ''],
      options_arabic: ['', '', ''],
      correct_answer: '',
      correct_answer_arabic: '',
      explanation: '',
      arabic_explanation: ''
    };
    
    const newWords = [...words];
    if (!newWords[currentWordIndex].questions) {
      newWords[currentWordIndex].questions = [];
    }
    newWords[currentWordIndex].questions.push(newQuestion);
    setWords(newWords);
    setCurrentQuestionIndex(newWords[currentWordIndex].questions.length - 1);
  };

  const removeQuestion = (wordIndex, questionIndex) => {
    const newWords = [...words];
    newWords[wordIndex].questions.splice(questionIndex, 1);
    setWords(newWords);
    
    // Adjust current question index
    const questionsLength = newWords[wordIndex].questions.length;
    if (currentQuestionIndex >= questionsLength && questionsLength > 0) {
      setCurrentQuestionIndex(questionsLength - 1);
    } else if (questionsLength === 0) {
      setCurrentQuestionIndex(0);
    }
  };

  const updateQuestion = (wordIndex, questionIndex, field, value) => {
    const newWords = [...words];
    if (!newWords[wordIndex].questions[questionIndex]) return;
    
    newWords[wordIndex].questions[questionIndex][field] = value;
    setWords(newWords);
  };

  const updateQuestionOption = (wordIndex, questionIndex, optionIndex, value, isArabic = false) => {
    const newWords = [...words];
    const question = newWords[wordIndex].questions[questionIndex];
    if (!question) return;
    
    const optionsField = isArabic ? 'options_arabic' : 'options';
    if (!question[optionsField]) {
      question[optionsField] = [];
    }
    
    // Ensure the options array is long enough
    while (question[optionsField].length <= optionIndex) {
      question[optionsField].push('');
    }
    
    question[optionsField][optionIndex] = value;
    setWords(newWords);
  };

  const addOption = (wordIndex, questionIndex) => {
    const newWords = [...words];
    const question = newWords[wordIndex].questions[questionIndex];
    if (!question) return;
    
    if (!question.options) question.options = [];
    if (!question.options_arabic) question.options_arabic = [];
    
    question.options.push('');
    question.options_arabic.push('');
    setWords(newWords);
  };

  const removeOption = (wordIndex, questionIndex, optionIndex) => {
    const newWords = [...words];
    const question = newWords[wordIndex].questions[questionIndex];
    if (!question || question.options.length <= 2) {
      Alert.alert('Error', 'At least 2 options are required');
      return;
    }
    
    question.options.splice(optionIndex, 1);
    question.options_arabic.splice(optionIndex, 1);
    setWords(newWords);
  };

  const handleSubmit = () => {
    // Validation
    if (!sentence.trim()) {
      Alert.alert('Error', 'Sentence is required');
      return;
    }

    const validWords = words.filter(word => word.text.trim());
    if (validWords.length === 0) {
      Alert.alert('Error', 'At least one word is required');
      return;
    }

    // Check each word has at least one complete question
    for (const word of validWords) {
      if (!word.questions || word.questions.length === 0) {
        Alert.alert('Error', `Word "${word.text}" needs at least one question`);
        return;
      }
      
      for (const question of word.questions) {
        if (!question.question.trim() || !question.correct_answer.trim()) {
          Alert.alert('Error', `Incomplete question for word "${word.text}"`);
          return;
        }
        
        const validOptions = question.options?.filter(opt => opt.trim()) || [];
        if (validOptions.length < 2) {
          Alert.alert('Error', `At least 2 options required for questions in word "${word.text}"`);
          return;
        }
      }
    }

    // Prepare the data
    const irabData = {
      sentence: sentence.trim(),
      words: validWords.map((word, index) => ({
        ...word,
        position: index,
        questions: word.questions.map(q => ({
          ...q,
          options: q.options?.filter(opt => opt.trim()) || [],
          options_arabic: q.options_arabic?.filter(opt => opt.trim()) || []
        }))
      }))
    };

    onSubmit(JSON.stringify(irabData));
  };

  const currentWord = words[currentWordIndex];
  const currentQuestion = currentWord?.questions?.[currentQuestionIndex];

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Create I'rab Analysis Exercise</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Sentence</Text>
        <TextInput
          style={styles.sentenceInput}
          value={sentence}
          onChangeText={setSentence}
          placeholder="Enter the Arabic sentence to analyze"
          placeholderTextColor="#95a5a6"
          multiline
        />
      </View>

      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Words ({words.length})</Text>
          <TouchableOpacity style={styles.addButton} onPress={addWord}>
            <Text style={styles.addButtonText}>+ Add Word</Text>
          </TouchableOpacity>
        </View>
        
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.wordsScroll}>
          {words.map((word, index) => (
            <TouchableOpacity
              key={index}
              style={[
                styles.wordChip,
                currentWordIndex === index && styles.activeWordChip
              ]}
              onPress={() => {
                setCurrentWordIndex(index);
                setCurrentQuestionIndex(0);
              }}
            >
              <Text style={[
                styles.wordChipText,
                currentWordIndex === index && styles.activeWordChipText
              ]}>
                {word.text || `Word ${index + 1}`}
              </Text>
              {words.length > 1 && (
                <TouchableOpacity
                  style={styles.removeWordButton}
                  onPress={() => removeWord(index)}
                >
                  <Text style={styles.removeWordButtonText}>×</Text>
                </TouchableOpacity>
              )}
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {currentWord && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>
            Edit Word {currentWordIndex + 1}
          </Text>
          <TextInput
            style={styles.input}
            value={currentWord.text}
            onChangeText={(text) => updateWordText(currentWordIndex, text)}
            placeholder="Enter word text"
            placeholderTextColor="#95a5a6"
          />
          
          <View style={styles.questionsHeader}>
            <Text style={styles.subsectionTitle}>
              Questions ({currentWord.questions?.length || 0})
            </Text>
            <TouchableOpacity style={styles.smallAddButton} onPress={addQuestion}>
              <Text style={styles.addButtonText}>+ Add Question</Text>
            </TouchableOpacity>
          </View>

          {currentWord.questions && currentWord.questions.length > 0 && (
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.questionsScroll}>
              {currentWord.questions.map((_, qIndex) => (
                <TouchableOpacity
                  key={qIndex}
                  style={[
                    styles.questionChip,
                    currentQuestionIndex === qIndex && styles.activeQuestionChip
                  ]}
                  onPress={() => setCurrentQuestionIndex(qIndex)}
                >
                  <Text style={[
                    styles.questionChipText,
                    currentQuestionIndex === qIndex && styles.activeQuestionChipText
                  ]}>
                    Q{qIndex + 1}
                  </Text>
                  <TouchableOpacity
                    style={styles.removeQuestionButton}
                    onPress={() => removeQuestion(currentWordIndex, qIndex)}
                  >
                    <Text style={styles.removeQuestionButtonText}>×</Text>
                  </TouchableOpacity>
                </TouchableOpacity>
              ))}
            </ScrollView>
          )}

          {currentQuestion && (
            <View style={styles.questionForm}>
              <Text style={styles.subsectionTitle}>Question {currentQuestionIndex + 1}</Text>
              
              <View style={styles.fieldContainer}>
                <Text style={styles.label}>Question (English)</Text>
                <TextInput
                  style={styles.textArea}
                  value={currentQuestion.question}
                  onChangeText={(value) => updateQuestion(currentWordIndex, currentQuestionIndex, 'question', value)}
                  placeholder="Enter question in English"
                  placeholderTextColor="#95a5a6"
                  multiline
                />
              </View>

              <View style={styles.fieldContainer}>
                <Text style={styles.label}>Question (Arabic)</Text>
                <TextInput
                  style={styles.textArea}
                  value={currentQuestion.question_arabic}
                  onChangeText={(value) => updateQuestion(currentWordIndex, currentQuestionIndex, 'question_arabic', value)}
                  placeholder="Enter question in Arabic"
                  placeholderTextColor="#95a5a6"
                  multiline
                />
              </View>

              <View style={styles.fieldContainer}>
                <View style={styles.sectionHeader}>
                  <Text style={styles.label}>Answer Options</Text>
                  <TouchableOpacity 
                    style={styles.smallAddButton} 
                    onPress={() => addOption(currentWordIndex, currentQuestionIndex)}
                  >
                    <Text style={styles.addButtonText}>+ Option</Text>
                  </TouchableOpacity>
                </View>
                
                {currentQuestion.options?.map((option, optIndex) => (
                  <View key={optIndex} style={styles.optionContainer}>
                    <Text style={styles.optionLabel}>Option {optIndex + 1}</Text>
                    <View style={styles.optionRow}>
                      <TextInput
                        style={[styles.optionInput, { flex: 1 }]}
                        value={option}
                        onChangeText={(value) => updateQuestionOption(currentWordIndex, currentQuestionIndex, optIndex, value)}
                        placeholder="English option"
                        placeholderTextColor="#95a5a6"
                      />
                      <TextInput
                        style={[styles.optionInput, { flex: 1, marginLeft: 10 }]}
                        value={currentQuestion.options_arabic?.[optIndex] || ''}
                        onChangeText={(value) => updateQuestionOption(currentWordIndex, currentQuestionIndex, optIndex, value, true)}
                        placeholder="Arabic option"
                        placeholderTextColor="#95a5a6"
                      />
                      {(currentQuestion.options?.length || 0) > 2 && (
                        <TouchableOpacity
                          style={styles.removeOptionButton}
                          onPress={() => removeOption(currentWordIndex, currentQuestionIndex, optIndex)}
                        >
                          <Text style={styles.removeOptionButtonText}>×</Text>
                        </TouchableOpacity>
                      )}
                    </View>
                  </View>
                ))}
              </View>

              <View style={styles.fieldContainer}>
                <Text style={styles.label}>Correct Answer (English)</Text>
                <TextInput
                  style={styles.input}
                  value={currentQuestion.correct_answer}
                  onChangeText={(value) => updateQuestion(currentWordIndex, currentQuestionIndex, 'correct_answer', value)}
                  placeholder="Enter correct answer in English"
                  placeholderTextColor="#95a5a6"
                />
              </View>

              <View style={styles.fieldContainer}>
                <Text style={styles.label}>Correct Answer (Arabic)</Text>
                <TextInput
                  style={styles.input}
                  value={currentQuestion.correct_answer_arabic}
                  onChangeText={(value) => updateQuestion(currentWordIndex, currentQuestionIndex, 'correct_answer_arabic', value)}
                  placeholder="Enter correct answer in Arabic"
                  placeholderTextColor="#95a5a6"
                />
              </View>

              <View style={styles.fieldContainer}>
                <Text style={styles.label}>Explanation (English)</Text>
                <TextInput
                  style={styles.textArea}
                  value={currentQuestion.explanation}
                  onChangeText={(value) => updateQuestion(currentWordIndex, currentQuestionIndex, 'explanation', value)}
                  placeholder="Enter explanation in English"
                  placeholderTextColor="#95a5a6"
                  multiline
                />
              </View>

              <View style={styles.fieldContainer}>
                <Text style={styles.label}>Explanation (Arabic)</Text>
                <TextInput
                  style={styles.textArea}
                  value={currentQuestion.arabic_explanation}
                  onChangeText={(value) => updateQuestion(currentWordIndex, currentQuestionIndex, 'arabic_explanation', value)}
                  placeholder="Enter explanation in Arabic"
                  placeholderTextColor="#95a5a6"
                  multiline
                />
              </View>
            </View>
          )}
        </View>
      )}

      {!hideButtons && (
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.cancelButton} onPress={onCancel}>
            <Text style={styles.cancelButtonText}>Cancel</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.submitButton} onPress={handleSubmit}>
            <Text style={styles.submitButtonText}>Save I'rab Analysis</Text>
          </TouchableOpacity>
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    backgroundColor: '#fff',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
    textAlign: 'center',
  },
  section: {
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#ecf0f1',
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 15,
  },
  subsectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#34495e',
    marginBottom: 10,
  },
  sentenceInput: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#dee2e6',
    borderRadius: 8,
    paddingHorizontal: 15,
    paddingVertical: 12,
    fontSize: 18,
    color: '#2c3e50',
    minHeight: 80,
    textAlignVertical: 'top',
  },
  wordsScroll: {
    flexDirection: 'row',
    marginBottom: 15,
  },
  wordChip: {
    backgroundColor: '#ecf0f1',
    paddingHorizontal: 15,
    paddingVertical: 10,
    borderRadius: 20,
    marginRight: 10,
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  activeWordChip: {
    backgroundColor: '#3498db',
    borderColor: '#2980b9',
  },
  wordChipText: {
    color: '#7f8c8d',
    fontWeight: '600',
    marginRight: 8,
  },
  activeWordChipText: {
    color: '#fff',
  },
  removeWordButton: {
    backgroundColor: 'rgba(231, 76, 60, 0.8)',
    borderRadius: 10,
    width: 20,
    height: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  removeWordButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  questionsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 20,
    marginBottom: 10,
  },
  questionsScroll: {
    flexDirection: 'row',
    marginBottom: 15,
  },
  questionChip: {
    backgroundColor: '#ecf0f1',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 15,
    marginRight: 8,
    flexDirection: 'row',
    alignItems: 'center',
  },
  activeQuestionChip: {
    backgroundColor: '#e67e22',
  },
  questionChipText: {
    color: '#7f8c8d',
    fontWeight: '600',
    marginRight: 6,
  },
  activeQuestionChipText: {
    color: '#fff',
  },
  removeQuestionButton: {
    backgroundColor: 'rgba(231, 76, 60, 0.8)',
    borderRadius: 8,
    width: 16,
    height: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  removeQuestionButtonText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  questionForm: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    marginTop: 10,
  },
  fieldContainer: {
    marginBottom: 15,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2c3e50',
    marginBottom: 8,
  },
  input: {
    backgroundColor: '#f8f9fa',
    borderWidth: 1,
    borderColor: '#dee2e6',
    borderRadius: 8,
    paddingHorizontal: 15,
    paddingVertical: 12,
    fontSize: 16,
    color: '#2c3e50',
  },
  textArea: {
    backgroundColor: '#f8f9fa',
    borderWidth: 1,
    borderColor: '#dee2e6',
    borderRadius: 8,
    paddingHorizontal: 15,
    paddingVertical: 12,
    fontSize: 16,
    color: '#2c3e50',
    minHeight: 80,
    textAlignVertical: 'top',
  },
  optionContainer: {
    marginBottom: 10,
  },
  optionLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#7f8c8d',
    marginBottom: 5,
  },
  optionRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  optionInput: {
    backgroundColor: '#f8f9fa',
    borderWidth: 1,
    borderColor: '#dee2e6',
    borderRadius: 6,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 14,
    color: '#2c3e50',
  },
  removeOptionButton: {
    backgroundColor: '#e74c3c',
    borderRadius: 15,
    width: 30,
    height: 30,
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 10,
  },
  removeOptionButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  addButton: {
    backgroundColor: '#27ae60',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 6,
  },
  smallAddButton: {
    backgroundColor: '#27ae60',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
  },
  addButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 20,
    gap: 15,
  },
  cancelButton: {
    flex: 1,
    backgroundColor: '#6c757d',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  cancelButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  submitButton: {
    flex: 1,
    backgroundColor: '#27ae60',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default IrabAnalysisForm;
