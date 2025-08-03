import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Export the base api for admin dashboard
export { api };

export const levelsAPI = {
  getLevels: () => api.get('/levels'),
  getLevel: (id) => api.get(`/levels/${id}`),
  getLessons: (levelId) => api.get(`/levels/${levelId}/lessons`),
  getNextLevel: (levelId) => api.get(`/levels/${levelId}/next`),
};

export const lessonsAPI = {
  getLesson: (id) => api.get(`/lessons/${id}`),
  getExercises: (lessonId) => api.get(`/lessons/${lessonId}/exercises`),
  getNextLesson: (lessonId) => api.get(`/lessons/${lessonId}/next`),
};

export const exercisesAPI = {
  getExercise: (id) => api.get(`/exercises/${id}`),
  checkAnswer: (exerciseId, userAnswer, userId = 'default_user') => 
    api.post(`/exercises/${exerciseId}/check`, {
      exercise_id: exerciseId,
      user_answer: userAnswer,
      user_id: userId,
    }),
};

export const userAPI = {
  getProgress: (userId) => api.get(`/users/${userId}/progress`),
  updateProgress: (userId, progress) => 
    api.post(`/users/${userId}/progress`, progress),
};
