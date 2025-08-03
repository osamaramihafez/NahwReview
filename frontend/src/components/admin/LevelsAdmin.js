import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { api } from '../../services/api';
import LevelForm from './LevelForm';

const LevelsAdmin = () => {
  const [levels, setLevels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingLevel, setEditingLevel] = useState(null);

  useEffect(() => {
    fetchLevels();
  }, []);

  const fetchLevels = async () => {
    try {
      setLoading(true);
      const response = await api.get('/levels');
      setLevels(response.data);
    } catch (error) {
      console.error('Error fetching levels:', error);
      Alert.alert('Error', 'Failed to fetch levels');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateLevel = () => {
    setEditingLevel(null);
    setShowForm(true);
  };

  const handleEditLevel = (level) => {
    setEditingLevel(level);
    setShowForm(true);
  };

  const handleFormSubmit = async (levelData) => {
    try {
      if (editingLevel) {
        // Update existing level
        await api.put(`/levels/${editingLevel.id}`, levelData);
      } else {
        // Create new level
        await api.post('/levels', levelData);
      }
      setShowForm(false);
      setEditingLevel(null);
      fetchLevels();
      Alert.alert('Success', editingLevel ? 'Level updated successfully' : 'Level created successfully');
    } catch (error) {
      console.error('Error saving level:', error);
      Alert.alert('Error', 'Failed to save level');
    }
  };

  const handleDeleteLevel = (levelId) => {
    Alert.alert(
      'Confirm Delete',
      'Are you sure you want to delete this level? This will also delete all associated lessons and exercises.',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Delete', 
          style: 'destructive',
          onPress: async () => {
            try {
              await api.delete(`/levels/${levelId}`);
              fetchLevels();
              Alert.alert('Success', 'Level deleted successfully');
            } catch (error) {
              console.error('Error deleting level:', error);
              Alert.alert('Error', 'Failed to delete level');
            }
          }
        }
      ]
    );
  };

  if (showForm) {
    return (
      <LevelForm
        level={editingLevel}
        onSubmit={handleFormSubmit}
        onCancel={() => {
          setShowForm(false);
          setEditingLevel(null);
        }}
      />
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Levels Management</Text>
        <TouchableOpacity style={styles.addButton} onPress={handleCreateLevel}>
          <Text style={styles.addButtonText}>+ Add Level</Text>
        </TouchableOpacity>
      </View>

      {loading ? (
        <Text style={styles.loadingText}>Loading levels...</Text>
      ) : (
        <ScrollView style={styles.levelsList}>
          {levels.map((level) => (
            <View key={level.id} style={styles.levelCard}>
              <View style={styles.levelHeader}>
                <View>
                  <Text style={styles.levelName}>{level.name}</Text>
                  <Text style={styles.levelOrder}>Order: {level.order}</Text>
                  {level.description && (
                    <Text style={styles.levelDescription}>{level.description}</Text>
                  )}
                </View>
                <View style={styles.levelActions}>
                  <TouchableOpacity
                    style={styles.editButton}
                    onPress={() => handleEditLevel(level)}
                  >
                    <Text style={styles.editButtonText}>Edit</Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    style={styles.deleteButton}
                    onPress={() => handleDeleteLevel(level.id)}
                  >
                    <Text style={styles.deleteButtonText}>Delete</Text>
                  </TouchableOpacity>
                </View>
              </View>
              <View style={styles.levelStats}>
                <Text style={styles.statsText}>
                  Lessons: {level.lessons ? level.lessons.length : 0}
                </Text>
              </View>
            </View>
          ))}
          {levels.length === 0 && (
            <Text style={styles.emptyText}>No levels found. Create your first level!</Text>
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
  loadingText: {
    textAlign: 'center',
    fontSize: 16,
    color: '#7f8c8d',
    marginTop: 50,
  },
  levelsList: {
    flex: 1,
  },
  levelCard: {
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
  levelHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 10,
  },
  levelName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 5,
  },
  levelOrder: {
    fontSize: 14,
    color: '#7f8c8d',
    marginBottom: 5,
  },
  levelDescription: {
    fontSize: 14,
    color: '#34495e',
    maxWidth: 250,
  },
  levelActions: {
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
  levelStats: {
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

export default LevelsAdmin;
