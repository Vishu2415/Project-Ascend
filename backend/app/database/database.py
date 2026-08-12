# it's a built-in module for work with SQLite database
import sqlite3

# it's use for manage the path of database by using path
from pathlib import Path

# here we define the location of database 
# if the ascend.db is not created yet so it will created automatically
DATABASE_PATH = Path("ascend.db")

# it's a funtion for creating a connection with database
def get_connection():
    
    # it return the connection of SQLite database
    return sqlite3.connect(DATABASE_PATH)

def create_table():
    
    # print("table created successfully") // i made this only for my testing purpose 
    
    connection = get_connection()
    
    cursor = connection.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL
        )
    """)
    
    connection.commit()
    
    connection.close()

# User kak prompt aur AI response database me save karne wala function
def save_messages(prompt: str, response: str):
    
    # Database connection create kr rhe hai 
    connection = get_connection()
    
    # SQL command execute krne ke liye cursor create kr rhe hai 
    cursor = connection.cursor()
    
    # Prompt or response ko message table me insert kr rhe hai
    cursor.execute(
        """
        INSERT INTO messages (prompt, response)
        VALUES (?, ?)
        """,
        (prompt, response)
    )
    
    # Insert ki hui information database me permanently save kar rahe hain.
    connection.commit()
    
    # Database connection close kar rahe hain.
    connection.close()
    
def get_messages():
     
     connection = get_connection()
     
     cursor = connection.cursor()
     
     cursor.execute(
         """
         SELECT id,prompt, response
         FROM messages
         """
         )
     messages = cursor.fetchall()
     
     connection.close()
     
     return messages
 
def get_recent_messages(limit: int=10):
     
     connection = get_connection()
     
     cursor = connection.cursor()
     
     cursor.execute(
         """
         SELECT prompt, response
         FROM messages 
         ORDER BY id DESC
         LIMIT ?
         """,
         (limit,)
         )
     
     messages = cursor.fetchall()
     
     connection.close()
     
     return messages
     
 
# NEW: Existing message ko update karne wala function.
def update_message(message_id: int, prompt: str, response: str):

    # Database connection create kar rahe hain.
    connection = get_connection()

    # SQL commands execute karne ke liye cursor create kar rahe hain.
    cursor = connection.cursor()

    # Given ID wale message ka prompt aur response update kar rahe hain.
    cursor.execute(
        """
        UPDATE messages
        SET prompt = ?, response = ?
        WHERE id = ?
        """,
        (prompt, response, message_id)  # NEW: SQL placeholders ki values pass kar rahe hain.
    )

    # Changes database mein save kar rahe hain.
    connection.commit()

    # Database connection close kar rahe hain.
    connection.close()
    
# NEW: Existing message ko delete karne wala function.
def delete_message(message_id: int):

    # Database connection create kar rahe hain.
    connection = get_connection()

    # SQL commands execute karne ke liye cursor create kar rahe hain.
    cursor = connection.cursor()

    # Given ID wale message ko delete kar rahe hain.
    cursor.execute(
        """
        DELETE FROM messages
        WHERE id = ?
        """,
        (message_id,)  # NEW: Single SQL parameter ko tuple ke form me pass kar rahe hain.
    )

    # Changes database mein save kar rahe hain.
    connection.commit()

    # Database connection close kar rahe hain.
    connection.close()