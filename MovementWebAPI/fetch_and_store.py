import requests
import sqlite3

def fetch_user_data(user_id):
    """Fetches user data and avatar image from the Reqres API."""
    response = requests.get(f'https://reqres.in/api/users/{user_id}')
    if response.status_code == 200:
        user_data = response.json()['data']

        # Fetch and store avatar image as BLOB
        avatar_response = requests.get(user_data['avatar'])
        if avatar_response.status_code == 200:
                    user_data['avatar_blob'] =  avatar_response.content
            
        else:
            user_data['avatar_blob'] = None  # Handle cases where the avatar image couldn't be fetched

        return user_data
    else:
        return None

def create_table(cursor):
    """Creates the 'users' table with the avatar as BLOB."""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            avatar BLOB NOT NULL
        )
    ''')

def insert_user(cursor, connection, user_data):
    """Inserts user data, including the avatar BLOB, into the 'users' table."""
    cursor.execute('''
        INSERT INTO users (id, email, firstName, lastName, avatar)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_data['id'], user_data['email'], user_data['first_name'], 
          user_data['last_name'], sqlite3.Binary( user_data['avatar_blob']) ))
    connection.commit()
    
    
def clear_table(cursor, connection):
    """Deletes all existing data from the 'users' table."""
    cursor.execute('DELETE FROM users')
    connection.commit()

def main():
    # Connect to SQLite database (or create it if not exists)
    connection = sqlite3.connect('reqres_data.db')
    cursor = connection.cursor()

    create_table(cursor)
    clear_table(cursor, connection)  # Clear the table before starting


    for user_id in range(1, 13):  # Fetch users 1 through 12
        user_data = fetch_user_data(user_id)
        if user_data:
            insert_user(cursor, connection, user_data)
            print(f"Inserted user {user_id}: {user_data['first_name']}")

    connection.close()

if __name__ == "__main__":
    main()