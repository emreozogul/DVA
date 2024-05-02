from database.db import DatabaseSingleton
from database.operations import DatabaseOperations
import eel
import wx
from prework.imageProcessing2 import process_image_4x, process_image_10x
from prework.model import predict_target

db = DatabaseSingleton()
conn = db.get_connection()
c = conn.cursor()
ops = DatabaseOperations(db)

@eel.expose
def add_project(name, owner, desc):
    ops.create_project(name=name, owner=owner , desc=desc)
    conn.commit()
    return "Project added successfully."
@eel.expose
def get_projects():   
    projects = ops.read_projects()
    simplified_projects = [{"id": project[0], "name": project[1], "owner": project[2], "description": project[3], "timestamp": project[4]} for project in projects]
    return simplified_projects

@eel.expose
def delete_project(projectName):
    ops.delete_project(projectName)
    conn.commit()
    return "Project deleted successfully."

@eel.expose
def select_image():
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard="*.tif;*.tiff", style=style)
    if dialog.ShowModal() == wx.ID_OK:
        image_path = dialog.GetPath()
    else:
        image_path = None
    dialog.Destroy()
    return image_path
 
@eel.expose
def check_project_exists(project_name):
    c.execute('SELECT * FROM projects WHERE name = ?', (project_name,))
    if c.fetchone():
        return True
    else:
        return False

@eel.expose
def get_project_data(project_name):
    cellsData = ops.get_cells_by_project_name(project_name)
    return cellsData
    

@eel.expose
def import_images(project_name, cell_name,  image_paths, scaleValues):
    length = len(image_paths)
    ops.create_cell(project_name, cell_name,length)
    conn.commit()
    id = ops.get_last_cell_id()
    for i in range(length):
        image_path = image_paths[i]
        scaleValue = scaleValues[i]
        phase_number = i + 1
        area_mm2, perimeter_mm, diameter_mm, roundness, aspect_ratio, solidity, convexity, particle_count = None, None, None, None, None, None, None, None
        if scaleValue == "4x":
            area_mm2, perimeter_mm, diameter_mm, roundness, aspect_ratio, solidity, convexity, particle_count = process_image_4x(image_path)
        elif scaleValue == "10x":
            area_mm2, perimeter_mm, diameter_mm, roundness, aspect_ratio, solidity, convexity, particle_count = process_image_10x(image_path)

        X = [[area_mm2, perimeter_mm, diameter_mm, roundness, aspect_ratio, solidity, convexity,
             particle_count]]
        viability = predict_target(X)
        
        ops.create_cell_phase(id, phase_number , area_mm2, perimeter_mm, diameter_mm, roundness,aspect_ratio, solidity, convexity, particle_count, scaleValue, viability)
        conn.commit()
    
@eel.expose
def get_cells_by_project_name(project_name):
    cells = ops.get_cells_by_project_name(project_name)
    return cells
        
    
if __name__ == '__main__':
    eel.init('web')  
    eel.init('web', allowed_extensions=['.js', '.html', '.css'])
    eel.start('index.html', size=(1000, 800), position=(100, 100))    
    