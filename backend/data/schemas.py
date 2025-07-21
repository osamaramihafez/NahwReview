from pydantic import BaseModel
from typing import List, Optional

class LevelBase(BaseModel):
    name: str
    description: Optional[str] = None
    order: int

class LevelCreate(LevelBase):
    pass

class Level(LevelBase):
    id: int
    lessons: Optional[List["Lesson"]] = []

class LessonBase(BaseModel):
    title: str
    arabic_title: Optional[str] = None
    description: Optional[str] = None
    order: int
    level_id: int

class LessonCreate(LessonBase):
    pass

class Lesson(LessonBase):
    id: int
    exercises: Optional[List["Exercise"]] = []

class ExerciseOptionBase(BaseModel):
    option_text: str
    is_correct: bool = False

class ExerciseOptionCreate(ExerciseOptionBase):
    pass

class ExerciseOption(ExerciseOptionBase):
    id: int
    exercise_id: int

class ExerciseBase(BaseModel):
    question: str
    question_arabic: Optional[str] = None
    exercise_type: str
    correct_answer: str
    explanation: Optional[str] = None
    order: int = 0
    lesson_id: int

class ExerciseCreate(ExerciseBase):
    options: List[ExerciseOptionCreate] = []

class Exercise(ExerciseBase):
    id: int
    options: List[ExerciseOption] = []

class UserProgressBase(BaseModel):
    user_id: str
    lesson_id: int
    completed: bool = False
    score: int = 0

class UserProgressCreate(UserProgressBase):
    pass

class UserProgress(UserProgressBase):
    id: int

class ExerciseAnswer(BaseModel):
    exercise_id: int
    user_answer: str
    user_id: str

# Update forward references
Level.model_rebuild()
Lesson.model_rebuild()
Exercise.model_rebuild()
