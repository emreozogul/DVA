from database.db import DatabaseSingleton
from database.operations import DatabaseOperations
import eel
import os
import wx
import pandas as pd
from prework.imageProcessing import process_image_4x, process_image_10x
from prework.model import predict_target , get_latest_csv_file
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
def paginate_project_data(project_name, page_number, page_size):
    cellsData = ops.paginate_cells_by_project_name(project_name, page_number, page_size)
    return cellsData

@eel.expose
def get_total_cells_count(project_name):
    return ops.count_cells_by_project_name(project_name)

@eel.expose
def import_images(project_name, cell_name,  image_paths, scaleValues):
    length = len(image_paths)
    ops.create_cell(project_name, cell_name,length)
    conn.commit()
    id = ops.get_last_cell_id()
    cell_results = []
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
        
        ops.create_cell_phase(id, phase_number, area_mm2, perimeter_mm, diameter_mm, roundness,aspect_ratio, solidity, convexity, particle_count, scaleValue, viability)
        conn.commit()
        
        cell_results.append({"cellName": cell_name, "phaseNo":phase_number, "area": area_mm2, "perimeter": perimeter_mm, "diameter": diameter_mm, "roundness": roundness,"aspectRatio": aspect_ratio,"solidity": solidity,"convexity": convexity, "particles" :particle_count,"scale": scaleValue,"viability": viability})
    
    return cell_results

@eel.expose
def add_to_model_data(phase_data):
    latest_csv_file = get_latest_csv_file()

    full_csv_path = os.path.join(latest_csv_file) if latest_csv_file else None

    if full_csv_path and os.path.exists(full_csv_path):
        data = pd.read_csv(full_csv_path)
    else:
        data = pd.DataFrame()
        
    if not isinstance(phase_data, pd.DataFrame):
        phase_data = pd.DataFrame([phase_data])

    data = pd.concat([data, phase_data], ignore_index=True)
    
    data.to_csv(full_csv_path, index=False)
    
    return "Data added to model successfully."

@eel.expose
def get_cells_by_project_name(project_name):
    cells = ops.get_cells_by_project_name(project_name)
    return cells

@eel.expose
def export_data(project_name):
    app = wx.App(False)
    dlg = wx.DirDialog(None, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
    
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath() 
        data = ops.getDataOfProject(project_name)
        column_names = ["project_id", "project_name", "cell_id", "cell_name", "phase_id", "phaseNumber", "area_mm2", "perimeter_mm", "diameter_mm", "roundness", "aspectRatio", "solidity", "convexity", "particleCount", "scaleValue", "viability"]
        df = pd.DataFrame(data, columns=column_names)
        df.to_csv(f"{path}/{project_name}.csv", index=False)
        result = "Success: File saved successfully."
    else:
        result = "Error: No directory selected."
    
    dlg.Destroy() 
    return result

if __name__ == '__main__':
    eel.init('web')  
    eel.init('web', allowed_extensions=['.js', '.html', '.css'])
    eel.start('index.html', size=(1000, 800), position=(100, 100))    
    