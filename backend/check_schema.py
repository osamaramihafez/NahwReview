import sqlite3

conn = sqlite3.connect('nahw_exercises.db')
cursor = conn.cursor()

print("Lessons table structure:")
cursor.execute('PRAGMA table_info(lessons)')
for row in cursor.fetchall():
    print(row)

print("\nLevels table structure:")
cursor.execute('PRAGMA table_info(levels)')
for row in cursor.fetchall():
    print(row)

print("\nExercises table structure:")
cursor.execute('PRAGMA table_info(exercises)')
for row in cursor.fetchall():
    print(row)

conn.close()
