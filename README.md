# Nahw Exercises - Arabic Grammar Learning App

A full-stack application for learning Arabic grammar (Nahw) with a React Native frontend, FastAPI backend, and SQLite database.

## Project Structure

```
NahwExercises/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database models and connection
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # Database operations
│   ├── populate_db.py       # Database population script
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── screens/         # Screen components
│   │   └── services/        # API services
│   ├── App.js              # Main application
│   ├── package.json        # Node.js dependencies
│   └── app.json            # Expo configuration
└── LessonContents.md       # Lesson curriculum outline
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```powershell
   cd backend
   ```

2. Create a virtual environment:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Populate the database:
   ```powershell
   python populate_db.py
   ```

5. Start the FastAPI server:
   ```powershell
   python main.py
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```powershell
   cd frontend
   ```

2. Install dependencies:
   ```powershell
   npm install
   ```

3. Start the Expo development server:
   ```powershell
   npm start
   ```

4. Use the Expo Go app on your phone to scan the QR code, or run on an emulator.

## API Endpoints

### Levels
- `GET /levels` - Get all levels
- `GET /levels/{level_id}` - Get a specific level
- `POST /levels` - Create a new level
- `GET /levels/{level_id}/lessons` - Get lessons for a level

### Lessons
- `GET /lessons/{lesson_id}` - Get a specific lesson
- `POST /lessons` - Create a new lesson
- `GET /lessons/{lesson_id}/exercises` - Get exercises for a lesson

### Exercises
- `GET /exercises/{exercise_id}` - Get a specific exercise
- `POST /exercises` - Create a new exercise
- `POST /exercises/{exercise_id}/check` - Check an answer

### User Progress
- `GET /users/{user_id}/progress` - Get user progress
- `POST /users/{user_id}/progress` - Update user progress

## Features

### Current Features
- 4 levels of Arabic grammar lessons
- Multiple choice and fill-in-the-blank exercises
- Progress tracking
- Arabic text support
- Clean, modern UI

### Planned Features
- User authentication
- Detailed progress analytics
- More exercise types
- Spaced repetition
- Achievement system
- Audio pronunciation
- Dark mode

## Technology Stack

- **Frontend**: React Native with Expo
- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **Navigation**: React Navigation
- **HTTP Client**: Axios

## Development Notes

- The app currently uses a default user ID for progress tracking
- Arabic text is displayed using serif font family
- The UI is designed with a green color scheme (#2E8B57)
- All Arabic grammar lessons are based on the curriculum in LessonContents.md
