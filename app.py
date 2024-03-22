from database.db import DatabaseSingleton
from database.operations import DatabaseOperations
import subprocess
import sys
import os
import eel
import base64
import numpy as np
import cv2
import wx
from prework.imageProcessing import process_image



# Initialize database connection
db = DatabaseSingleton()
conn = db.get_connection()
c = conn.cursor()

# Initialize database operations
ops = DatabaseOperations(db)


@eel.expose
def add_project(name, owner):
    ops.create_project(name=name, owner=owner)
    conn.commit()
    return "Project added successfully!"

@eel.expose
def get_projects():
    ops.read_projects()
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
def select_and_process_image():
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard="*.png;*.jpg;*.jpeg", style=style)
    if dialog.ShowModal() == wx.ID_OK:
        image_path = dialog.GetPath()
        # Process the image using the file path
        result_path = process_image(image_path)
    else:
        result_path = None
    dialog.Destroy()
    return result_path

 
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