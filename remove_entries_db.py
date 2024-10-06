import sqlite3

def clear_donations_table():
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect('donations.db')
        cursor = connection.cursor()

        # Execute the SQL query to delete all rows from the donations table
        cursor.execute('DELETE FROM donations')

        # Commit the changes
        connection.commit()

        # Close the connection
        connection.close()

        print("All entries from the donations table have been removed.")
    except Exception as e:
        print(f"Error clearing the donations table: {e}")

# Call the function to clear the table
clear_donations_table()
