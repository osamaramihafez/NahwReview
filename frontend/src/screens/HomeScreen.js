import React, { useState, useEffect } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  FlatList, 
  ActivityIndicator,
  Alert 
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
        <Text style={styles.title}>Nahw Exercises</Text>
        <Text style={styles.subtitle}>Master Arabic Grammar</Text>
        <Text style={styles.arabicTitle}>تمارين النحو</Text>
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
    alignItems: 'center',
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
  levelsList: {
    paddingTop: 20,
    paddingBottom: 20,
  },
});

export default HomeScreen;
