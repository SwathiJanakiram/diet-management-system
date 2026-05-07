import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect("diet_management_system.db")
cursor = conn.cursor()

# Values to match
user_id = "Swathi J7899423192"
day = '4/1/25'

# Execute delete query
cursor.execute("DELETE FROM daily_calorie_intake WHERE user_id = ? AND day = ?", (user_id, day))

# Commit the changes and close connection
conn.commit()
conn.close()
