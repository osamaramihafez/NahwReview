# Scripts to Remove

The following scripts are no longer needed in our clean irab-focused backend:

## Conversion Scripts (can be removed):
- convert_all_to_irab.py
- convert_fill_blank.py 
- convert_to_bilingual.py
- convert_to_clean_bilingual.py

## Old Exercise Scripts (can be removed):
- add_irab_exercises.py (replaced by setup_clean_irab_curriculum.py)
- add_comprehensive_irab_exercises.py (replaced by setup_clean_irab_curriculum.py)
- create_intermediate_exercises.py
- populate_db.py

## Old Testing Scripts (can be removed):
- test_bilingual.py
- test_conversion.py
- test_irab_exercises.py

## Database Maintenance Scripts (can be removed):
- add_order_column.py
- clear_db.py (functionality merged into setup script)

## Scripts to Keep:
- main.py (FastAPI server)
- database.py (database setup)
- schemas.py (data models)
- crud.py (database operations)
- requirements.txt (dependencies)
- check_database.py (useful for debugging)
- check_db.py (if different from check_database.py)
- check_lessons.py (useful for verification)
- show_exercise_summary.py (useful for verification)
- setup_clean_irab_curriculum.py (new main setup script)
- check_schema.py (useful for database inspection)

Let's remove the unnecessary scripts to clean up the backend.
