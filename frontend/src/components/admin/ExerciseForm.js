import React, { useState } from 'react';
import { View, Text, TextInput, StyleSheet, TouchableOpacity, ScrollView, Alert } from 'react-native';
import IrabAnalysisForm from './IrabAnalysisForm';

const ExerciseForm = ({ exercise, lessons, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    question: exercise?.question || '',
    question_arabic: exercise?.question_arabic || '',
    exercise_type: exercise?.exercise_type || 'multiple_choice',
    correct_answer: exercise?.correct_answer || '',
    explanation: exercise?.explanation || '',
    order: exercise?.order?.toString() || '',
    lesson_id: exercise?.lesson_id?.toString() || '',
  });

  const [options, setOptions] = useState(
    exercise?.options || [
      { option_text: '', is_correct: false },
      { option_text: '', is_correct: false },
    ]
  );

  const [errors, setErrors] = useState({});

  const exerciseTypes = [
    { id: 'multiple_choice', name: 'Multiple Choice' },
    { id: 'irab_analysis', name: 'I\'rab Analysis' },
    { id: 'fill_blank', name: 'Fill in the Blank' },
  ];

  const validateForm = () => {
    const newErrors = {};

    if (!formData.question.trim()) {
      newErrors.question = 'Question is required';
    }

    if (!formData.lesson_id) {
      newErrors.lesson_id = 'Please select a lesson';
    }

    if (!formData.correct_answer.trim()) {
      newErrors.correct_answer = 'Correct answer is required';
    }

    if (!formData.order.trim()) {
      newErrors.order = 'Order is required';
    } else if (isNaN(parseInt(formData.order))) {
      newErrors.order = 'Order must be a number';
    }

    // Validate multiple choice options
    if (formData.exercise_type === 'multiple_choice') {
      const validOptions = options.filter(opt => opt.option_text.trim());
      if (validOptions.length < 2) {
        newErrors.options = 'At least 2 options are required for multiple choice';
      }

      const correctOptions = options.filter(opt => opt.is_correct && opt.option_text.trim());
      if (correctOptions.length === 0) {
        newErrors.options = 'At least one option must be marked as correct';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validateForm()) {
      const exerciseData = {
        question: formData.question.trim(),
        question_arabic: formData.question_arabic.trim() || null,
        exercise_type: formData.exercise_type,
        correct_answer: formData.correct_answer.trim(),
        explanation: formData.explanation.trim() || null,
        order: parseInt(formData.order),
        lesson_id: parseInt(formData.lesson_id),
      };

      // Add options for multiple choice exercises
      if (formData.exercise_type === 'multiple_choice') {
        exerciseData.options = options
          .filter(opt => opt.option_text.trim())
          .map(opt => ({
            option_text: opt.option_text.trim(),
            is_correct: opt.is_correct,
          }));
      }

      onSubmit(exerciseData);
    }
  };

  const updateField = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  };

  const updateOption = (index, field, value) => {
    const newOptions = [...options];
    newOptions[index] = { ...newOptions[index], [field]: value };
    
    // If marking this option as correct for single-correct exercises, unmark others
    if (field === 'is_correct' && value === true) {
      newOptions.forEach((opt, i) => {
        if (i !== index) opt.is_correct = false;
      });
    }
    
    setOptions(newOptions);
    
    // Clear options error
    if (errors.options) {
      setErrors(prev => ({ ...prev, options: null }));
    }
  };

  const addOption = () => {
    setOptions([...options, { option_text: '', is_correct: false }]);
  };

  const removeOption = (index) => {
    if (options.length > 2) {
      setOptions(options.filter((_, i) => i !== index));
    } else {
      Alert.alert('Error', 'At least 2 options are required');
    }
  };

  const groupedLessons = lessons.reduce((acc, lesson) => {
    if (!acc[lesson.level_name]) {
      acc[lesson.level_name] = [];
    }
    acc[lesson.level_name].push(lesson);
    return acc;
  }, {});

  // If this is an I'rab analysis exercise, show the specialized form
  if (formData.exercise_type === 'irab_analysis') {
    let irabSubmitFunction = null;

    const handleMainSubmit = () => {
      // Validate main form fields first
      const newErrors = {};
      if (!formData.question.trim()) {
        newErrors.question = 'Exercise title is required';
      }
      if (!formData.lesson_id) {
        newErrors.lesson_id = 'Please select a lesson';
      }
      if (!formData.order.trim()) {
        newErrors.order = 'Order is required';
      } else if (isNaN(parseInt(formData.order))) {
        newErrors.order = 'Order must be a number';
      }

      setErrors(newErrors);
      if (Object.keys(newErrors).length > 0) {
        return;
      }

      // If main form is valid, trigger I'rab form validation
      if (irabSubmitFunction) {
        irabSubmitFunction();
      }
    };

    const handleIrabSubmit = (irabData) => {
      const exerciseData = {
        question: formData.question.trim(),
        question_arabic: formData.question_arabic.trim() || null,
        exercise_type: 'irab_analysis',
        correct_answer: irabData, // Store the JSON as the correct answer
        explanation: formData.explanation.trim() || null,
        order: parseInt(formData.order),
        lesson_id: parseInt(formData.lesson_id),
        options: [] // I'rab exercises don't use the standard options
      };
      onSubmit(exerciseData);
    };

    return (
      <ScrollView style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.title}>
            {exercise ? 'Edit I\'rab Analysis Exercise' : 'Create I\'rab Analysis Exercise'}
          </Text>
        </View>

        <View style={styles.form}>
          <View style={styles.fieldContainer}>
            <Text style={styles.label}>Lesson *</Text>
            <ScrollView style={styles.lessonSelector} showsVerticalScrollIndicator={false}>
              {Object.entries(groupedLessons).map(([levelName, levelLessons]) => (
                <View key={levelName} style={styles.levelGroup}>
                  <Text style={styles.levelGroupTitle}>{levelName}</Text>
                  {levelLessons.map((lesson) => (
                    <TouchableOpacity
                      key={lesson.id}
                      style={[
                        styles.lessonOption,
                        formData.lesson_id === lesson.id.toString() && styles.selectedLesson
                      ]}
                      onPress={() => updateField('lesson_id', lesson.id.toString())}
                    >
                      <Text style={[
                        styles.lessonOptionText,
                        formData.lesson_id === lesson.id.toString() && styles.selectedLessonText
                      ]}>
                        {lesson.title}
                      </Text>
                    </TouchableOpacity>
                  ))}
                </View>
              ))}
            </ScrollView>
            {errors.lesson_id && <Text style={styles.errorText}>{errors.lesson_id}</Text>}
          </View>

          <View style={styles.fieldContainer}>
            <Text style={styles.label}>Exercise Title *</Text>
            <TextInput
              style={[styles.textArea, errors.question && styles.inputError]}
              value={formData.question}
              onChangeText={(value) => updateField('question', value)}
              placeholder="Enter a title/description for this I'rab exercise"
              placeholderTextColor="#95a5a6"
              multiline={true}
              numberOfLines={2}
              textAlignVertical="top"
            />
            {errors.question && <Text style={styles.errorText}>{errors.question}</Text>}
          </View>

          <View style={styles.fieldContainer}>
            <Text style={styles.label}>Arabic Title</Text>
            <TextInput
              style={[styles.textArea, errors.question_arabic && styles.inputError]}
              value={formData.question_arabic}
              onChangeText={(value) => updateField('question_arabic', value)}
              placeholder="Enter Arabic title/description (optional)"
              placeholderTextColor="#95a5a6"
              multiline={true}
              numberOfLines={2}
              textAlignVertical="top"
            />
          </View>

          <View style={styles.fieldContainer}>
            <Text style={styles.label}>Order *</Text>
            <TextInput
              style={[styles.input, errors.order && styles.inputError]}
              value={formData.order}
              onChangeText={(value) => updateField('order', value)}
              placeholder="Enter display order within the lesson (1, 2, 3...)"
              placeholderTextColor="#95a5a6"
              keyboardType="numeric"
            />
            {errors.order && <Text style={styles.errorText}>{errors.order}</Text>}
          </View>

          <View style={styles.fieldContainer}>
            <Text style={styles.label}>General Explanation</Text>
            <TextInput
              style={[styles.textArea, errors.explanation && styles.inputError]}
              value={formData.explanation}
              onChangeText={(value) => updateField('explanation', value)}
              placeholder="Enter general explanation for this exercise (optional)"
              placeholderTextColor="#95a5a6"
              multiline={true}
              numberOfLines={3}
              textAlignVertical="top"
            />
          </View>
        </View>

        <View style={styles.irabFormContainer}>
          <IrabAnalysisForm
            onSubmit={handleIrabSubmit}
            onCancel={onCancel}
            onValidate={(submitFn) => { irabSubmitFunction = submitFn; }}
            initialData={exercise?.correct_answer ? JSON.parse(exercise.correct_answer) : null}
            hideButtons={true}
          />
        </View>

        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.cancelButton} onPress={onCancel}>
            <Text style={styles.cancelButtonText}>Cancel</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.submitButton} onPress={handleMainSubmit}>
            <Text style={styles.submitButtonText}>
              {exercise ? 'Update Exercise' : 'Create Exercise'}
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>
          {exercise ? 'Edit Exercise' : 'Create New Exercise'}
        </Text>
      </View>

      <View style={styles.form}>
        <View style={styles.fieldContainer}>
          <Text style={styles.label}>Exercise Type *</Text>
          <View style={styles.typeContainer}>
            {exerciseTypes.map((type) => (
              <TouchableOpacity
                key={type.id}
                style={[
                  styles.typeOption,
                  formData.exercise_type === type.id && styles.selectedType
                ]}
                onPress={() => updateField('exercise_type', type.id)}
              >
                <Text style={[
                  styles.typeOptionText,
                  formData.exercise_type === type.id && styles.selectedTypeText
                ]}>
                  {type.name}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        <View style={styles.fieldContainer}>
          <Text style={styles.label}>Lesson *</Text>
          <ScrollView style={styles.lessonSelector} showsVerticalScrollIndicator={false}>
            {Object.entries(groupedLessons).map(([levelName, levelLessons]) => (
              <View key={levelName} style={styles.levelGroup}>
                <Text style={styles.levelGroupTitle}>{levelName}</Text>
                {levelLessons.map((lesson) => (
                  <TouchableOpacity
                    key={lesson.id}
                    style={[
                      styles.lessonOption,
                      formData.lesson_id === lesson.id.toString() && styles.selectedLesson
                    ]}
                    onPress={() => updateField('lesson_id', lesson.id.toString())}
                  >
                    <Text style={[
                      styles.lessonOptionText,
                      formData.lesson_id === lesson.id.toString() && styles.selectedLessonText
                    ]}>
                      {lesson.title}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            ))}
          </ScrollView>
          {errors.lesson_id && <Text style={styles.errorText}>{errors.lesson_id}</Text>}
        </View>

        <View style={styles.fieldContainer}>
          <Text style={styles.label}>Question *</Text>
          <TextInput
            style={[styles.textArea, errors.question && styles.inputError]}
            value={formData.question}
            onChangeText={(value) => updateField('question', value)}
            placeholder="Enter the exercise question in English"
            placeholderTextColor="#95a5a6"
            multiline={true}
            numberOfLines={3}
            textAlignVertical="top"
          />
          {errors.question && <Text style={styles.errorText}>{errors.question}</Text>}
        </View>

        <View style={styles.fieldContainer}>
          <Text style={styles.label}>Arabic Question</Text>
          <TextInput
            style={[styles.textArea, errors.question_arabic && styles.inputError]}
            value={formData.question_arabic}
            onChangeText={(value) => updateField('question_arabic', value)}
            placeholder="Enter the exercise question in Arabic (optional)"
            placeholderTextColor="#95a5a6"
            multiline={true}
            numberOfLines={3}
            textAlignVertical="top"
          />
        </View>

        <View style={styles.fieldContainer}>
          <Text style={styles.label}>Correct Answer *</Text>
          <TextInput
            style={[styles.input, errors.correct_answer && styles.inputError]}
            value={formData.correct_answer}
            onChangeText={(value) => updateField('correct_answer', value)}
            placeholder="Enter the correct answer"
            placeholderTextColor="#95a5a6"
          />
          {errors.correct_answer && <Text style={styles.errorText}>{errors.correct_answer}</Text>}
        </View>

        {/* Multiple Choice Options */}
        {formData.exercise_type === 'multiple_choice' && (
          <View style={styles.fieldContainer}>
            <Text style={styles.label}>Answer Options *</Text>
            {options.map((option, index) => (
              <View key={index} style={styles.optionContainer}>
                <View style={styles.optionRow}>
                  <TextInput
                    style={[styles.optionInput, errors.options && styles.inputError]}
                    value={option.option_text}
                    onChangeText={(value) => updateOption(index, 'option_text', value)}
                    placeholder={`Option ${index + 1}`}
                    placeholderTextColor="#95a5a6"
                  />
                  <TouchableOpacity
                    style={[styles.correctCheckbox, option.is_correct && styles.correctCheckboxActive]}
                    onPress={() => updateOption(index, 'is_correct', !option.is_correct)}
                  >
                    <Text style={[
                      styles.checkboxText,
                      option.is_correct && styles.checkboxTextActive
                    ]}>
                      ✓
                    </Text>
                  </TouchableOpacity>
                  {options.length > 2 && (
                    <TouchableOpacity
                      style={styles.removeButton}
                      onPress={() => removeOption(index)}
                    >
                      <Text style={styles.removeButtonText}>×</Text>
                    </TouchableOpacity>
                  )}
                </View>
              </View>
            ))}
            <TouchableOpacity style={styles.addOptionButton} onPress={addOption}>
              <Text style={styles.addOptionText}>+ Add Option</Text>
            </TouchableOpacity>
            {errors.options && <Text style={styles.errorText}>{errors.options}</Text>}
          </View>
        )}

        <View style={styles.fieldContainer}>
          <Text style={styles.label}>Explanation</Text>
          <TextInput
            style={[styles.textArea, errors.explanation && styles.inputError]}
            value={formData.explanation}
            onChangeText={(value) => updateField('explanation', value)}
            placeholder="Enter explanation for the correct answer (optional)"
            placeholderTextColor="#95a5a6"
            multiline={true}
            numberOfLines={4}
            textAlignVertical="top"
          />
        </View>

        <View style={styles.fieldContainer}>
          <Text style={styles.label}>Order *</Text>
          <TextInput
            style={[styles.input, errors.order && styles.inputError]}
            value={formData.order}
            onChangeText={(value) => updateField('order', value)}
            placeholder="Enter display order within the lesson (1, 2, 3...)"
            placeholderTextColor="#95a5a6"
            keyboardType="numeric"
          />
          {errors.order && <Text style={styles.errorText}>{errors.order}</Text>}
        </View>

        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.cancelButton} onPress={onCancel}>
            <Text style={styles.cancelButtonText}>Cancel</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.submitButton} onPress={handleSubmit}>
            <Text style={styles.submitButtonText}>
              {exercise ? 'Update Exercise' : 'Create Exercise'}
            </Text>
          </TouchableOpacity>
        </View>
      </View>
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
  form: {
    padding: 20,
  },
  fieldContainer: {
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2c3e50',
    marginBottom: 8,
  },
  typeContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
  },
  typeOption: {
    backgroundColor: '#ecf0f1',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 8,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  selectedType: {
    backgroundColor: '#3498db',
    borderColor: '#2980b9',
  },
  typeOptionText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#7f8c8d',
  },
  selectedTypeText: {
    color: '#fff',
  },
  lessonSelector: {
    maxHeight: 200,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#dee2e6',
    borderRadius: 8,
    padding: 10,
  },
  levelGroup: {
    marginBottom: 15,
  },
  levelGroupTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#7f8c8d',
    marginBottom: 8,
    textTransform: 'uppercase',
  },
  lessonOption: {
    backgroundColor: '#f8f9fa',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 6,
    marginBottom: 4,
    borderWidth: 1,
    borderColor: 'transparent',
  },
  selectedLesson: {
    backgroundColor: '#3498db',
    borderColor: '#2980b9',
  },
  lessonOptionText: {
    fontSize: 14,
    color: '#2c3e50',
  },
  selectedLessonText: {
    color: '#fff',
    fontWeight: '600',
  },
  input: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#dee2e6',
    borderRadius: 8,
    paddingHorizontal: 15,
    paddingVertical: 12,
    fontSize: 16,
    color: '#2c3e50',
  },
  textArea: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#dee2e6',
    borderRadius: 8,
    paddingHorizontal: 15,
    paddingVertical: 12,
    fontSize: 16,
    color: '#2c3e50',
    minHeight: 80,
  },
  inputError: {
    borderColor: '#e74c3c',
  },
  optionContainer: {
    marginBottom: 10,
  },
  optionRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  optionInput: {
    flex: 1,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#dee2e6',
    borderRadius: 8,
    paddingHorizontal: 15,
    paddingVertical: 12,
    fontSize: 16,
    color: '#2c3e50',
  },
  correctCheckbox: {
    width: 40,
    height: 40,
    borderWidth: 2,
    borderColor: '#dee2e6',
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  correctCheckboxActive: {
    backgroundColor: '#27ae60',
    borderColor: '#27ae60',
  },
  checkboxText: {
    fontSize: 18,
    color: '#dee2e6',
    fontWeight: 'bold',
  },
  checkboxTextActive: {
    color: '#fff',
  },
  removeButton: {
    width: 40,
    height: 40,
    backgroundColor: '#e74c3c',
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  removeButtonText: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },
  addOptionButton: {
    backgroundColor: '#ecf0f1',
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  addOptionText: {
    color: '#7f8c8d',
    fontWeight: '600',
  },
  errorText: {
    color: '#e74c3c',
    fontSize: 14,
    marginTop: 5,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 30,
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
  irabFormContainer: {
    flex: 1,
  },
});

export default ExerciseForm;
