# Nahw Exercises - Arabic Grammar Learning App

A comprehensive full-stack application for learning Arabic grammar (Nahw) with bilingual support, featuring a React Native frontend, FastAPI backend, SQLite database, and a modular translation system.

## 📖 Table of Contents

- [Project Overview](#project-overview)
- [Database Structure](#database-structure)
- [Translation System](#translation-system)
- [Backend Scripts](#backend-scripts)
- [Frontend Structure](#frontend-structure)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Development Workflow](#development-workflow)

## 🎯 Project Overview

This application helps users learn Arabic grammar through structured lessons and exercises. It supports bilingual content (Arabic/English) with plans for additional languages. The app features:

- **Hierarchical Learning Structure**: Levels → Lessons → Exercises
- **Multiple Exercise Types**: Multiple choice, fill-in-the-blank, irab analysis
- **Bilingual Support**: Arabic and English content with modular translation system
- **Progress Tracking**: User progress across lessons and exercises
- **Modern Tech Stack**: React Native frontend, FastAPI backend, SQLite database

## 🗄️ Database Structure

### Core Tables

#### `levels` - Learning Levels
Organizes content into difficulty levels.
```sql
CREATE TABLE levels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,                -- "Level 1 - Basic Sentences"
    arabic_name TEXT,                  -- "المستوى الأول - الجمل البسيطة"
    description TEXT,                  -- English description
    arabic_description TEXT,           -- Arabic description
    "order" INTEGER NOT NULL           -- Display order
);
```

#### `lessons` - Individual Lessons
Contains specific grammar topics within levels.
```sql
CREATE TABLE lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,               -- "Verbal Sentences - Past Tense"
    arabic_title TEXT,                 -- "الجملة الفعلية - الفعل الماضي"
    description TEXT,                  -- English description
    arabic_description TEXT,           -- Arabic description
    "order" INTEGER NOT NULL,          -- Order within level
    level_id INTEGER NOT NULL,         -- References levels(id)
    FOREIGN KEY (level_id) REFERENCES levels (id)
);
```

#### `exercises` - Practice Exercises
Individual questions and activities.
```sql
CREATE TABLE exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,            -- "What type of word is 'كَتَبَ'?"
    question_arabic TEXT,              -- "ما نوع الكلمة 'كَتَبَ'؟"
    exercise_type TEXT NOT NULL,       -- "multiple_choice", "irab_analysis"
    correct_answer TEXT NOT NULL,      -- Expected answer
    explanation TEXT,                  -- English explanation
    arabic_explanation TEXT,           -- Arabic explanation
    "order" INTEGER DEFAULT 0,         -- Order within lesson
    lesson_id INTEGER NOT NULL,        -- References lessons(id)
    FOREIGN KEY (lesson_id) REFERENCES lessons (id)
);
```

### Translation System Tables

#### `translation_keys` - Translation References
Central repository for translatable terms.
```sql
CREATE TABLE translation_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_name TEXT UNIQUE NOT NULL,     -- "verb", "noun", "nominative"
    category TEXT,                     -- "parts_of_speech", "grammatical_case"
    description TEXT                   -- Optional description
);
```

#### `translations` - Multi-language Translations
Actual translations in different languages.
```sql
CREATE TABLE translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    translation_key_id INTEGER NOT NULL,
    language_code TEXT NOT NULL,       -- "ar", "en", "fr", "es"
    text TEXT NOT NULL,                -- "فعل", "verb", "verbe"
    is_primary BOOLEAN DEFAULT 0,      -- Primary translation for language
    FOREIGN KEY (translation_key_id) REFERENCES translation_keys (id),
    UNIQUE(translation_key_id, language_code, text)
);
```

#### `exercise_options` - Exercise Answer Options
Support both translation keys and direct text.
```sql
CREATE TABLE exercise_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    translation_key_id INTEGER,        -- Optional: references translation_keys(id)
    option_text TEXT,                  -- Direct text fallback
    is_correct BOOLEAN DEFAULT 0,      -- Is this the correct answer?
    exercise_id INTEGER NOT NULL,      -- References exercises(id)
    FOREIGN KEY (translation_key_id) REFERENCES translation_keys (id),
    FOREIGN KEY (exercise_id) REFERENCES exercises (id)
);
```

### User Progress Table

#### `user_progress` - Learning Progress Tracking
```sql
CREATE TABLE user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,             -- User identifier
    lesson_id INTEGER NOT NULL,        -- References lessons(id)
    completed BOOLEAN DEFAULT 0,       -- Has user completed lesson?
    score INTEGER DEFAULT 0,           -- User's score on lesson
    FOREIGN KEY (lesson_id) REFERENCES lessons (id)
);
```

## 🌍 Translation System

The app uses a modular translation system that eliminates the need to store duplicate content in multiple languages.

### Pre-populated Translation Categories

#### Parts of Speech (`parts_of_speech`)
- `verb` → "فعل" (AR) / "verb" (EN)
- `noun` → "اسم" (AR) / "noun" (EN)
- `particle` → "حرف" (AR) / "particle" (EN)

#### Verb Tenses (`verb_tense`)
- `past_tense` → "ماض" (AR) / "past" (EN)
- `present_tense` → "مضارع" (AR) / "present" (EN)
- `imperative` → "أمر" (AR) / "imperative" (EN)

#### Grammatical Cases (`grammatical_case`)
- `nominative` → "مرفوع" (AR) / "nominative" (EN)
- `accusative` → "منصوب" (AR) / "accusative" (EN)
- `genitive` → "مجرور" (AR) / "genitive" (EN)
- `jussive` → "مجزوم" (AR) / "jussive" (EN)

#### Sentence Elements (`sentence_element`)
- `subject_doer` → "فاعل" (AR) / "doer/subject" (EN)
- `direct_object` → "مفعول به" (AR) / "direct object" (EN)
- `subject_nominal` → "مبتدأ" (AR) / "subject" (EN)
- `predicate` → "خبر" (AR) / "predicate" (EN)

### Benefits
- ✅ Consistent terminology across all exercises
- ✅ Easy language addition (French, Spanish, etc.)
- ✅ Centralized translation management
- ✅ Reduced database size
- ✅ Support for mixed content (translation keys + direct text)

## 🔧 Backend Scripts

### Core Application Files

#### `main.py` - FastAPI Application
- **Purpose**: Main REST API server
- **Features**: CRUD endpoints for levels, lessons, exercises, user progress
- **Key Endpoints**: `/levels`, `/lessons`, `/exercises`, `/users/{user_id}/progress`
- **Dependencies**: FastAPI, SQLite via aiosqlite

#### `database.py` - Database Connection & Schema
- **Purpose**: Database initialization and connection management
- **Features**: Creates all tables, handles connections
- **Functions**: `init_database()`, `get_db()`

#### `schemas.py` - Pydantic Data Models
- **Purpose**: API request/response validation
- **Models**: `Level`, `Lesson`, `Exercise`, `ExerciseOption`, `UserProgress`
- **Features**: Type validation, JSON serialization

#### `crud.py` - Database Operations
- **Purpose**: Database CRUD operations
- **Features**: All database queries and mutations
- **Functions**: `get_levels()`, `create_exercise()`, `check_answer()`, etc.

### Database Setup & Management

#### `update_schema.py` - Database Schema Creation
- **Purpose**: Create/recreate database tables with latest schema
- **Usage**: `python update_schema.py`
- **Features**: Drops existing tables, creates new schema with translation support
- **⚠️ Warning**: Destructive operation - backs up existing data first

#### `database.py` - Alternative Schema Setup
- **Purpose**: Non-destructive database initialization
- **Usage**: Called automatically by FastAPI app
- **Features**: Creates tables if they don't exist (uses `CREATE TABLE IF NOT EXISTS`)

### Translation System Scripts

#### `create_translation_system.py` - Translation System Setup
- **Purpose**: Initialize modular translation system
- **Features**: 
  - Creates `translation_keys` and `translations` tables
  - Populates 22 common grammatical terms
  - Sets up Arabic and English translations
- **Usage**: `python create_translation_system.py`

#### `migrate_to_translation_system.py` - Data Migration
- **Purpose**: Migrate existing exercise options to translation system
- **Features**:
  - Analyzes existing options for translation candidates
  - Creates translation keys for common terms
  - Migrates data to new `exercise_options_v2` table
- **Usage**: `python migrate_to_translation_system.py`

#### `fix_english_translations.py` - Translation Corrections
- **Purpose**: Update English translations to proper terms
- **Features**: Replaces Arabic text in English translations with actual English
- **Usage**: `python fix_english_translations.py`

#### `demo_translation_system.py` - Translation Demo
- **Purpose**: Demonstrate translation system functionality
- **Features**:
  - Creates sample exercises using translation keys
  - Shows language switching (Arabic ↔ English)
  - Demonstrates mixed content support
- **Usage**: `python demo_translation_system.py`

### Content Management Scripts

#### `curriculum_data.json` - Curriculum Data (JSON Format)
- **Purpose**: Contains all curriculum data in structured JSON format
- **Content**: 2 levels, 5 lessons, 5 comprehensive exercises focused on irab analysis
- **Structure**: Levels, lessons, exercises with full bilingual support
- **Features**: Human-readable, version-controllable, language-agnostic
- **Usage**: Edit directly or use validation/loading scripts

#### `load_curriculum.py` - JSON-to-Database Loader
- **Purpose**: Populate database from JSON curriculum data
- **Features**: 
  - Clears existing data safely
  - Loads levels, lessons, and exercises from JSON
  - Provides detailed progress feedback
  - Shows curriculum summary after loading
- **Usage**: `python load_curriculum.py`

#### `validate_curriculum.py` - JSON Validation
- **Purpose**: Validate curriculum JSON structure and content
- **Features**:
  - Checks required fields and data types
  - Validates ID uniqueness and references
  - Provides detailed error reporting
  - Shows statistics (total questions, etc.)
- **Usage**: `python validate_curriculum.py`

#### `setup_clean_irab_curriculum.py` - Legacy Curriculum Setup (Deprecated)
- **Purpose**: Original Python-based curriculum setup
- **Status**: ⚠️ Deprecated - Use JSON-based system instead
- **Migration**: Data moved to `curriculum_data.json`
- **Usage**: Archived for reference only

#### `create_intermediate_exercises.py` - Exercise Creation
- **Purpose**: Bulk create intermediate-level exercises
- **Features**: Creates 100+ exercises across multiple lessons
- **Content**: Covers verb tenses, sentence types, grammatical analysis
- **Usage**: `python create_intermediate_exercises.py`

#### `add_comprehensive_irab_exercises.py` - Irab Analysis
- **Purpose**: Add complex grammatical analysis exercises
- **Features**: Multi-step irab analysis with word-by-word breakdown
- **Usage**: `python add_comprehensive_irab_exercises.py`

#### `populate_db.py` - Basic Data Population
- **Purpose**: Add sample data to empty database
- **Features**: Creates basic levels, lessons, exercises
- **Usage**: `python populate_db.py`

### Utility & Analysis Scripts

#### `check_database.py` - Database Inspection
- **Purpose**: Examine database contents and structure
- **Features**: Shows table counts, sample data
- **Usage**: `python check_database.py`

#### `check_lessons.py` - Lesson Analysis
- **Purpose**: Display lessons and their exercises
- **Features**: Shows lesson structure, exercise counts
- **Usage**: `python check_lessons.py`

#### `check_schema.py` - Schema Validation
- **Purpose**: Verify database schema integrity
- **Features**: Checks table structure, relationships
- **Usage**: `python check_schema.py`

#### `check_table_structure.py` - Table Structure
- **Purpose**: Show detailed table column information
- **Features**: PRAGMA table_info for all tables
- **Usage**: `python check_table_structure.py`

#### `curriculum_summary.py` - Content Overview
- **Purpose**: Generate curriculum summary report
- **Features**: Shows levels, lessons, exercise counts
- **Usage**: `python curriculum_summary.py`

#### `show_exercise_summary.py` - Exercise Analysis
- **Purpose**: Detailed exercise statistics and content
- **Features**: Exercise types, difficulty distribution
- **Usage**: `python show_exercise_summary.py`

#### `verify_correct_answers.py` - Answer Validation
- **Purpose**: Verify exercise answers are properly formatted
- **Features**: Checks answer consistency, finds errors
- **Usage**: `python verify_correct_answers.py`

### Helper & Example Scripts

#### `translation_crud_additions.py` - Translation Functions
- **Purpose**: Helper functions for translation system
- **Features**: `get_translation()`, `create_exercise_with_translated_options()`
- **Usage**: Import functions into main application

#### `translation_system_example.py` - Complete Example
- **Purpose**: Comprehensive translation system usage examples
- **Features**: Shows admin functions, bulk operations, workflows
- **Usage**: `python translation_system_example.py`

## 📱 Frontend Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ExerciseCard.js           # Exercise container component
│   │   ├── MultipleChoiceExercise.js # Multiple choice questions
│   │   ├── IrabAnalysisExercise.js   # Grammatical analysis exercises
│   │   ├── LessonCard.js             # Lesson display component
│   │   └── LevelCard.js              # Level display component
│   ├── screens/
│   │   ├── HomeScreen.js             # Main navigation screen
│   │   ├── LessonsScreen.js          # Lesson selection screen
│   │   └── ExercisesScreen.js        # Exercise practice screen
│   └── services/
│       └── api.js                    # API communication layer
├── App.js                            # Main application component
├── package.json                      # Dependencies and scripts
└── app.json                          # Expo configuration
```

## 🚀 Setup Instructions

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

## 🚀 Setup Instructions

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Initialize Database**
   ```bash
   # Option 1: Full schema recreation (destructive)
   python update_schema.py
   
   # Option 2: Safe initialization
   python -c "import asyncio; from database import init_database; asyncio.run(init_database())"
   ```

3. **Set Up Translation System**
   ```bash
   python create_translation_system.py
   python fix_english_translations.py
   ```

4. **Populate with Content**
   ```bash
   # Basic content
   python populate_db.py
   
   # Or comprehensive curriculum
   python create_intermediate_exercises.py
   python add_comprehensive_irab_exercises.py
   ```

5. **Start Server**
   ```bash
   python main.py
   # Server runs on http://localhost:8000
   ```

### Frontend Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**
   ```bash
   npx expo start
   ```

3. **Run on Device/Emulator**
   - Scan QR code with Expo Go app (mobile)
   - Press 'i' for iOS simulator
   - Press 'a' for Android emulator

## 🔌 API Endpoints

### Levels
- `GET /levels` - Get all levels
- `GET /levels/{level_id}` - Get specific level
- `POST /levels` - Create new level
- `GET /levels/{level_id}/lessons` - Get lessons for level

### Lessons  
- `GET /lessons/{lesson_id}` - Get specific lesson
- `POST /lessons` - Create new lesson
- `GET /lessons/{lesson_id}/exercises` - Get exercises for lesson

### Exercises
- `GET /exercises/{exercise_id}` - Get specific exercise
- `POST /exercises` - Create new exercise
- `POST /exercises/{exercise_id}/check` - Check answer

### User Progress
- `GET /users/{user_id}/progress` - Get user progress
- `POST /users/{user_id}/progress` - Update progress

### Translation System (Future)
- `GET /exercises/{exercise_id}?language=en` - Get localized exercise
- `GET /translations/{key}?language=ar` - Get specific translation

## 🔄 Development Workflow

### JSON-Based Curriculum Management (Recommended)

1. **Validate Current Data**
   ```bash
   cd backend
   python validate_curriculum.py
   ```

2. **Edit Curriculum Data**
   - Open `curriculum_data.json` in your editor
   - Make changes to levels, lessons, or exercises
   - Ensure proper JSON structure and encoding

3. **Validate Changes**
   ```bash
   python validate_curriculum.py
   ```

4. **Load into Database**
   ```bash
   python load_curriculum.py
   ```

5. **Test Backend**
   ```bash
   python main.py  # Start the API server
   ```

### Adding New Content (JSON Method)

1. **Add New Level**
   ```json
   {
     "id": 3,
     "name": "Level 3 - Advanced Grammar",
     "arabic_name": "المستوى الثالث - النحو المتقدم",
     "description": "Advanced grammatical structures",
     "arabic_description": "التراكيب النحوية المتقدمة",
     "order": 3
   }
   ```

2. **Add New Lesson**
   ```json
   {
     "id": 6,
     "title": "Conditional Sentences",
     "arabic_title": "الجمل الشرطية",
     "description": "Learn about conditional structures",
     "arabic_description": "تعلم التراكيب الشرطية",
     "order": 1,
     "level_id": 3
   }
   ```

3. **Add New Exercise**
   ```json
   {
     "id": 6,
     "question": "Analyze the following sentence grammatically",
     "question_arabic": "حلل الجملة التالية نحوياً",
     "exercise_type": "irab_analysis",
     "lesson_id": 6,
     "order": 1,
     "explanation": "Example explanation",
     "arabic_explanation": "شرح المثال",
     "data": {"sentence": "إن تدرس تنجح", "words": [...]}
   }
   ```

### Legacy Python-Based Content Management

1. **Create Exercise with Translation Keys**
   ```python
   exercise_data = {
       "question": "What type of word is this?",
       "question_arabic": "ما نوع هذه الكلمة؟",
       "options": [
           {"translation_key": "verb", "is_correct": True},
           {"translation_key": "noun", "is_correct": False}
       ]
   }
   ```

2. **Add New Translation Key**
   ```python
   await create_translation_key(db, "new_term", "category", {
       "ar": "النص العربي",
       "en": "English text"
   })
   ```

3. **Test Changes**
   ```bash
   python demo_translation_system.py
   python check_database.py
   ```

### Database Maintenance

1. **Check Database Status**
   ```bash
   python check_database.py
   python curriculum_summary.py
   ```

2. **Verify Data Integrity**
   ```bash
   python verify_correct_answers.py
   python check_schema.py
   ```

3. **Backup Before Changes**
   ```bash
   cp nahw_exercises.db nahw_exercises_backup.db
   ```

### Adding New Languages

1. **Add Translations to Existing Keys**
   ```python
   # Add French translations
   french_translations = {"verb": "verbe", "noun": "nom"}
   for key, text in french_translations.items():
       await add_translation(db, key, "fr", text)
   ```

2. **Update API to Support New Language**
   ```python
   @app.get("/exercises/{exercise_id}")
   async def get_exercise(exercise_id: int, language: str = "ar"):
       return await get_exercise_localized(db, exercise_id, language)
   ```

## 📋 Project Summary

- **25+ Python scripts** covering database management, content creation, and translation system
- **8 database tables** with comprehensive relationships and bilingual support  
- **Modular translation system** supporting unlimited languages
- **React Native frontend** with clean component architecture
- **RESTful API** with FastAPI and async/await support
- **SQLite database** with proper foreign key relationships

This application demonstrates modern full-stack development practices with particular attention to internationalization, modular design, and educational content management.

## 🏗️ Recent Additions

### Translation System Implementation
The app now features a comprehensive modular translation system that:
- Eliminates duplicate storage of Arabic/English content
- Supports easy addition of new languages
- Centralizes terminology management
- Maintains consistency across all exercises

### Irab Analysis Exercises
Advanced grammatical analysis exercises where users analyze Arabic sentences word by word:
- Identify word types (فعل, اسم, حرف)
- Determine grammatical cases (مرفوع, منصوب, مجرور, مجزوم)
- Multi-step analysis with immediate feedback
- Interactive word-by-word progression

### Comprehensive Script Collection
Over 25 specialized scripts for different aspects of the application:
- Database management and schema updates
- Content creation and population
- Translation system setup and migration
- Analysis and verification tools
- Demo and example implementations
