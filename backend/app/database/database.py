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
            session_id TEXT NOT NULL,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL
        )
    """)
    
    # NEW: Har session ki conversation summary store karne ke liye table create kar rahe hain.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS session_summaries(
            session_id TEXT PRIMARY KEY,
            summary TEXT NOT NULL
        )
        """
        )
    
    # NEW: Existing database me session_id column check kar rahe hain.
    cursor.execute("PRAGMA table_info(messages)")
     
    # NEW: Existing columns ki information read kar rahe hain.
    columns = [column[1] for column in cursor.fetchall()]
    
    # NEW: Agar session_id column nahi hai to add kar rahe hain. 
    if "session_id" not in columns:
        cursor.execute(
            "ALTER TABLE messages ADD COLUMN session_id TEXT"
        )
    
    # NEW: Column add hone ke baad existing messages ke liye default session set kar rahe hain.
    cursor.execute(
        """
        UPDATE messages
        SET session_id = 'default'
        WHERE session_id is NULL
        """
        )    
     
    connection.commit()
    
    connection.close()

# User kak prompt aur AI response database me save karne wala function
def save_messages(prompt: str, response: str, session_id:str):
    
    # Database connection create kr rhe hai 
    connection = get_connection()
    
    # SQL command execute krne ke liye cursor create kr rhe hai 
    cursor = connection.cursor()
    
    # Prompt or response ko message table me insert kr rhe hai
    # NEW: Message ko uske session ke saath database me insert kar rahe hain.
    cursor.execute(
        """
        INSERT INTO messages (session_id, prompt, response)
        VALUES (?, ?, ?)
        """,
        (session_id, prompt, response)
    )
    
    # Insert ki hui information database me permanently save kar rahe hain.
    connection.commit()
    
    # Database connection close kar rahe hain.
    connection.close()

def save_session_summary(session_id: str, summary: str):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO session_summaries (session_id, summary)
        VALUES (?, ?)
        """,
        (session_id, summary)
    )

    connection.commit()

    connection.close()    

def get_session_summary(session_id: str):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT summary
        FROM session_summaries
        WHERE session_id = ?
        """,
        (session_id,)
    )

    result = cursor.fetchone()

    connection.close()

    return result[0] if result else ""
    
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
 
def get_recent_messages(session_id: str, limit: int=10):
     
     connection = get_connection()
     
     cursor = connection.cursor()
     
     # NEW: Sirf given session ki recent conversation history nikal rahe hain.
     cursor.execute(
         """
         SELECT prompt, response
         FROM messages 
         WHERE session_id = ?
         ORDER BY id DESC
         LIMIT ?
         """,
         (session_id, limit)
         )
     
     messages = cursor.fetchall()
     
     connection.close()
     
     return messages

# NEW: Current session me total messages count karne wala function.
def get_message_count(session_id: str):
    
    # Database connection create kar rahe hain.
    connection = get_connection()
    
    # SQL commands execute karne ke liye cursor create kar rahe hain.
    cursor = connection.cursor()
    
    # NEW: Given session ke total messages count kar rahe hain.
    cursor.execute(
    """
    SELECT COUNT(*)
    FROM messages
    WHERE session_id = ?
    """,
    (session_id,)
    )
    
    # Count ka result retrieve kar rahe hain.
    count = cursor.fetchone()[0]
     
    # Database connection close kar rahe hain.
    connection.close()
    
    # Total message count return kar rahe hain.
    return count
         
 
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