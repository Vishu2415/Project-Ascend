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