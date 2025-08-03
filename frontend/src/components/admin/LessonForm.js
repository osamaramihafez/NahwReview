import React, { useState } from 'react';
import { View, Text, TextInput, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';

const LessonForm = ({ lesson, levels, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    title: lesson?.title || '',
    arabic_title: lesson?.arabic_title || '',
    description: lesson?.description || '',
    order: lesson?.order?.toString() || '',
    level_id: lesson?.level_id?.toString() || '',
  });

  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Lesson title is required';
    }

    if (!formData.level_id) {
      newErrors.level_id = 'Please select a level';
    }

    if (!formData.order.trim()) {
      newErrors.order = 'Order is required';
    } else if (isNaN(parseInt(formData.order))) {
      newErrors.order = 'Order must be a number';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validateForm()) {
      onSubmit({
        title: formData.title.trim(),
        arabic_title: formData.arabic_title.trim() || null,
        description: formData.description.trim() || null,
        order: parseInt(formData.order),
        level_id: parseInt(formData.level_id),
      });
    }
  };

  const updateField = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>
          {lesson ? 'Edit Lesson' : 'Create New Lesson'}
        </Text>
      </View>

      <View style={styles.form}>
        <View style={styles.fieldContainer}>
          <Text style={styles.label}>Level *</Text>
          <View style={styles.pickerContainer}>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.levelPicker}>
              {levels.map((level) => (
                <TouchableOpacity
                  key={level.id}
                  style={[
                    styles.levelOption,
                    formData.level_id === level.id.toString() && styles.selectedLevel
                  ]}
                  onPress={() => updateField('level_id', level.id.toString())}
                >
                  <Text style={[
                    styles.levelOptionText,
                    formData.level_id === level.id.toString() && styles.selectedLevelText
                  ]}>
                    {level.name}
                  </Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>
          {errors.level_id && <Text style={styles.errorText}>{errors.level_id}</Text>}
        </View>

        <View style={styles.fieldContainer}>
          <Text style={styles.label}>Lesson Title *</Text>
          <TextInput
            style={[styles.input, errors.title && styles.inputError]}
            value={formData.title}
            onChangeText={(value) => updateField('title', value)}
            placeholder="Enter lesson title in English"
            placeholderTextColor="#95a5a6"
          />
          {errors.title && <Text style={styles.errorText}>{errors.title}</Text>}
        </View>

        <View style={styles.fieldContainer}>
          <Text style={styles.label}>Arabic Title</Text>
          <TextInput
            style={[styles.input, errors.arabic_title && styles.inputError]}
            value={formData.arabic_title}
            onChangeText={(value) => updateField('arabic_title', value)}
            placeholder="Enter lesson title in Arabic (optional)"
            placeholderTextColor="#95a5a6"
          />
          {errors.arabic_title && <Text style={styles.errorText}>{errors.arabic_title}</Text>}
        </View>

        <View style={styles.fieldContainer}>
          <Text style={styles.label}>Description</Text>
          <TextInput
            style={[styles.textArea, errors.description && styles.inputError]}
            value={formData.description}
            onChangeText={(value) => updateField('description', value)}
            placeholder="Enter lesson description (optional)"
            placeholderTextColor="#95a5a6"
            multiline={true}
            numberOfLines={4}
            textAlignVertical="top"
          />
          {errors.description && <Text style={styles.errorText}>{errors.description}</Text>}
        </View>

        <View style={styles.fieldContainer}>
          <Text style={styles.label}>Order *</Text>
          <TextInput
            style={[styles.input, errors.order && styles.inputError]}
            value={formData.order}
            onChangeText={(value) => updateField('order', value)}
            placeholder="Enter display order within the level (1, 2, 3...)"
            placeholderTextColor="#95a5a6"
            keyboardType="numeric"
          />
          {errors.order && <Text style={styles.errorText}>{errors.order}</Text>}
          <Text style={styles.helpText}>
            Lower numbers appear first within the selected level.
          </Text>
        </View>

        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.cancelButton} onPress={onCancel}>
            <Text style={styles.cancelButtonText}>Cancel</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.submitButton} onPress={handleSubmit}>
            <Text style={styles.submitButtonText}>
              {lesson ? 'Update Lesson' : 'Create Lesson'}
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
  pickerContainer: {
    marginBottom: 10,
  },
  levelPicker: {
    flexDirection: 'row',
  },
  levelOption: {
    backgroundColor: '#ecf0f1',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    marginRight: 10,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  selectedLevel: {
    backgroundColor: '#3498db',
    borderColor: '#2980b9',
  },
  levelOptionText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#7f8c8d',
  },
  selectedLevelText: {
    color: '#fff',
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
    minHeight: 100,
  },
  inputError: {
    borderColor: '#e74c3c',
  },
  errorText: {
    color: '#e74c3c',
    fontSize: 14,
    marginTop: 5,
  },
  helpText: {
    color: '#6c757d',
    fontSize: 14,
    marginTop: 5,
    fontStyle: 'italic',
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
});

export default LessonForm;
