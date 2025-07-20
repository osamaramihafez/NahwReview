import sqlite3

# Check current table structure
conn = sqlite3.connect('nahw_exercises.db')
cursor = conn.execute('PRAGMA table_info(exercise_options)')
print('Current exercise_options structure:')
for row in cursor.fetchall():
    print(f"  Column: {row[1]}, Type: {row[2]}, NotNull: {row[3]}, Default: {row[4]}")

# Check if we need to modify the table
print(f"\nTables in database:")
cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
for row in cursor.fetchall():
    print(f"  • {row[0]}")

conn.close()
