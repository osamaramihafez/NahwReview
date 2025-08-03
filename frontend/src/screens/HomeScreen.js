import React, { useState, useEffect } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  FlatList, 
  ActivityIndicator,
  Alert,
  TouchableOpacity 
} from 'react-native';
import { levelsAPI } from '../services/api';
import LevelCard from '../components/LevelCard';

const HomeScreen = ({ navigation }) => {
  const [levels, setLevels] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLevels();
  }, []);

  const fetchLevels = async () => {
    try {
      const response = await levelsAPI.getLevels();
      setLevels(response.data);
    } catch (error) {
      console.error('Error fetching levels:', error);
      Alert.alert('Error', 'Failed to load levels. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleLevelPress = (level) => {
    navigation.navigate('Lessons', { level });
  };

  const renderLevel = ({ item }) => (
    <LevelCard 
      level={item} 
      onPress={() => handleLevelPress(item)} 
    />
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2E8B57" />
        <Text style={styles.loadingText}>Loading levels...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.headerContent}>
          <View style={styles.titleSection}>
            <Text style={styles.title}>Nahw Exercises through Qasas Al-Nabiyeen</Text>
            <Text style={styles.arabicTitle}>تمارين النحو بكتاب قصص النبيين</Text>
          </View>
          <TouchableOpacity 
            style={styles.adminButton}
            onPress={() => navigation.navigate('AdminLogin')}
          >
            <Text style={styles.adminButtonText}>⚙️ Admin</Text>
          </TouchableOpacity>
        </View>
      </View>
      
      <FlatList
        data={levels}
        renderItem={renderLevel}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.levelsList}
        showsVerticalScrollIndicator={false}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f7fa',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f7fa',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  header: {
    backgroundColor: '#2E8B57',
    paddingTop: 60,
    paddingBottom: 30,
    paddingHorizontal: 20,
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  titleSection: {
    alignItems: 'flex-start',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    color: '#e8f5e8',
    marginBottom: 8,
  },
  arabicTitle: {
    fontSize: 20,
    color: '#ffffff',
    fontFamily: 'serif',
  },
  adminButton: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.3)',
  },
  adminButtonText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '600',
  },
  levelsList: {
    paddingTop: 20,
    paddingBottom: 20,
  },
});

export default HomeScreen;
