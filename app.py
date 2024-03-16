import subprocess
import sys
import eel
import os
import sqlite3


# Initialize database connection
conn = sqlite3.connect('con.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT, author TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

@eel.expose
def add_project(name, author):
    c.execute('INSERT INTO projects (name, author) VALUES (?, ?)', (name, author))
    conn.commit()
    return "Project added successfully!"

@eel.expose
def get_projects():
    c.execute('SELECT * FROM projects ORDER BY created_at DESC')
    return c.fetchall()


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")

@eel.expose  # Expose this function to the JavaScript
def create_new_folder(folder_name):
    create_folder(folder_name)
    
@eel.expose
def check_project_name(project_name):
    c.execute('SELECT * FROM projects WHERE name = ?', (project_name,))
    # check if the project name already exists
    if c.fetchone():
        return True
    else:
        return False

# This function will be assigned to an input in js  
@eel.expose
def run_processing_and_model():
    python_path = sys.executable
    processing_py_path = "prework/processing.py"
    try:
        # Run the processing.py file
        print("Running the processing.py file...")
        subprocess.run([python_path, processing_py_path], check=True)
        print("processing.py file executed successfully.")
    except subprocess.CalledProcessError as e:
        print("An error occurred while running the processing.py file:", e)
        raise    
    
if __name__ == '__main__':
    eel.init('web')  # Give folder containing web files
    eel.start('index.html', size=(1000, 800) )    # Start