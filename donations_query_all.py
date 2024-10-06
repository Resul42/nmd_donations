import sqlite3

def get_all_donations():
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect('donations.db')
        cursor = connection.cursor()

        # Execute a query to fetch all rows from the donations table
        cursor.execute('SELECT * FROM donations')

        # Fetch all results
        donations = cursor.fetchall()

        # Close the connection
        connection.close()

        return donations
    except Exception as e:
        print(f"Error fetching donations: {e}")
        return []

# Example usage
donations = get_all_donations()

# Print the donations
for donation in donations:
    print(donation)
