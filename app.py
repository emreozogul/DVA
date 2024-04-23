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

db = DatabaseSingleton()
conn = db.get_connection()
c = conn.cursor()
ops = DatabaseOperations(db)

@eel.expose
def add_project(name, owner, desc):
    print(f"Adding project: {name} - {owner}")
    ops.create_project(name=name, owner=owner , desc=desc)
    conn.commit()
    return "Project added successfully."
@eel.expose
def get_projects():   
    projects = ops.read_projects()
    simplified_projects = [{"id": project[0], "name": project[1], "owner": project[2], "description": project[3], "timestamp": project[4]} for project in projects]
    return simplified_projects

@eel.expose  
def create_new_folder(folder_name):
    # Create a new folder in the current directory with the given name inside the "projects" folder
    folder_path = os.path.join(os.getcwd(), "projects", folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

@eel.expose
def delete_project(projetName):
    ops.delete_project(projetName)
    folder_path = os.path.join(os.getcwd(), "projects", projetName)
    os.rmdir(folder_path)
    conn.commit()
    return "Project deleted successfully."

@eel.expose
def select_and_process_image():
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard="*.png;*.jpg;*.jpeg;*.tif", style=style)
    if dialog.ShowModal() == wx.ID_OK:
        image_path = dialog.GetPath()
        result_path = process_image(image_path)
    else:
        result_path = None
    dialog.Destroy()
    return result_path


@eel.expose
def select_image():
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard="*.png;*.jpg;*.jpeg;*.tif", style=style)
    if dialog.ShowModal() == wx.ID_OK:
        image_path = dialog.GetPath()
    else:
        image_path = None
    dialog.Destroy()
    return image_path
 
@eel.expose
def check_project_exists(project_name):
    c.execute('SELECT * FROM projects WHERE name = ?', (project_name,))
    # check if the project name already exists
    if c.fetchone():
        return True
    else:
        return False
    
@eel.expose
def new_cell(projectName, image_paths):
    x = 0
    #fetch the last cell id and increment it by 1
    c.execute('SELECT MAX(cell_id) FROM cells')
    last_cell_id = c.fetchone()[0]
    if last_cell_id is None:
        last_cell_id = 0
    else:
        last_cell_id += 1
        
    c.execute('SELECT id FROM projects WHERE name = ?', (projectName,))
    project_id = c.fetchone()[0]
    
    results = []
    for image_path in image_paths:
        result = process_image(image_path) #process the image and get the results
        # new features can be added here
        perimeter = 5 #result["perimeter"] 
        area = 10  # result["area"]
        diameter = 2 # result["diameter"]
        classification = 0 # result["classification"]
        values = (last_cell_id, project_id, x, image_path, area, perimeter, diameter, classification)
        x += 1 
        results.append(result)
        add_cell(values)
        
    return results
          
def add_cell(values):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cells (cell_id, project_id, phase, image_name, area_mm2, perimeter_mm, diameter_mm, class) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", values)
    conn.commit()


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
    #set constaints for the window size min 500x500 and max 1000x800
    eel.init('web', allowed_extensions=['.js', '.html', '.css'])
    eel.start('index.html', size=(1000, 800), position=(100, 100))    
    