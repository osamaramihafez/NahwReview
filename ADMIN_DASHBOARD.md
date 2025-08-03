# Admin Dashboard Setup

## Overview
The admin dashboard provides a comprehensive interface for managing the Nahw Exercises application content. You can create, edit, and delete levels, lessons, and exercises without needing to modify the database directly.

## Features

### 📚 Levels Management
- **Create Levels**: Add new difficulty levels (e.g., Beginner, Intermediate, Advanced)
- **Edit Levels**: Modify level names, descriptions, and display order
- **Delete Levels**: Remove levels (this will also delete all associated lessons and exercises)
- **View Level Stats**: See how many lessons each level contains

### 📖 Lessons Management
- **Create Lessons**: Add new lessons to any level
- **Edit Lessons**: Modify lesson titles (English and Arabic), descriptions, and order
- **Delete Lessons**: Remove lessons (this will also delete all associated exercises)
- **Filter by Level**: View lessons for specific levels
- **View Lesson Stats**: See how many exercises each lesson contains

### ✏️ Exercises Management
- **Create Exercises**: Add new exercises to any lesson with support for:
  - Multiple Choice questions with customizable options
  - I'rab Analysis exercises
  - Fill in the Blank exercises
- **Edit Exercises**: Modify questions, answers, explanations, and options
- **Delete Exercises**: Remove individual exercises
- **Filter by Lesson**: View exercises for specific lessons
- **Question Types**: Support for English and Arabic questions

## How to Access

1. **Start the Backend Server**:
   ```bash
   cd backend
   python main.py
   ```
   The server will run on `http://localhost:8001`

2. **Start the Frontend**:
   ```bash
   cd frontend
   npm start
   ```

3. **Access Admin Dashboard**:
   - On the home screen, click the "⚙️ Admin" button in the top-right corner
   - Or navigate directly to the Admin route

## Usage Guide

### Creating Content Hierarchy

1. **Start with Levels**: Create your difficulty levels first (e.g., "Beginner", "Intermediate", "Advanced")
2. **Add Lessons**: For each level, create lessons that focus on specific grammar topics
3. **Create Exercises**: For each lesson, add various types of exercises

### Best Practices

- **Use Clear Naming**: Make level and lesson names descriptive
- **Order Management**: Use the order field to control how content appears to students
- **Arabic Support**: Add Arabic titles and questions for bilingual support
- **Explanations**: Always provide explanations for correct answers to help students learn

### Exercise Types

1. **Multiple Choice**:
   - Add 2-6 answer options
   - Mark the correct option(s)
   - Students select from the provided choices

2. **I'rab Analysis**:
   - Interactive grammar analysis exercises
   - Students analyze sentence structure
   - Automatic completion detection

3. **Fill in the Blank**:
   - Students type the correct answer
   - Exact match validation against the correct answer

## API Endpoints

The admin dashboard uses these API endpoints:

### Levels
- `GET /levels` - Get all levels
- `POST /levels` - Create a new level
- `PUT /levels/{id}` - Update a level
- `DELETE /levels/{id}` - Delete a level

### Lessons
- `GET /levels/{level_id}/lessons` - Get lessons for a level
- `POST /lessons` - Create a new lesson
- `PUT /lessons/{id}` - Update a lesson
- `DELETE /lessons/{id}` - Delete a lesson

### Exercises
- `GET /lessons/{lesson_id}/exercises` - Get exercises for a lesson
- `POST /exercises` - Create a new exercise
- `PUT /exercises/{id}` - Update an exercise
- `DELETE /exercises/{id}` - Delete an exercise

## Security Note

**⚠️ Important**: This admin dashboard currently has no authentication. In a production environment, you should:
- Add user authentication
- Implement role-based access control
- Secure the admin routes
- Add audit logging for content changes

## Troubleshooting

### Backend Issues
- Ensure Python dependencies are installed: `pip install -r requirements.txt`
- Check that the database file exists and is writable
- Verify the server is running on the correct port (8001)

### Frontend Issues
- Ensure Node.js dependencies are installed: `npm install`
- Check that the API base URL is correctly configured in `src/services/api.js`
- Verify the backend server is accessible

### Common Problems
- **Import Errors**: Make sure all Python modules are in the correct directories
- **CORS Issues**: The backend is configured to allow cross-origin requests
- **Database Errors**: Check that the SQLite database is properly initialized
