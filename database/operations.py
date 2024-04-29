class DatabaseOperations:
    def __init__(self, db):
        self.db = db
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close_connection()

    def create_project(self, name, owner, desc):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO projects (name, owner ,desc) VALUES (?, ?, ?)", (name, owner, desc))
        conn.commit()

    def read_projects(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects")
        return cursor.fetchall()
    
    def read_single_project(self, project_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        return cursor.fetchone()

    def delete_project(self, project_name):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE name = ?", (project_name,))
        conn.commit()

    def create_cell(self, project_name, name, phase_number):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM projects WHERE name = ?", (project_name,))
        project_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO cells (project_id, projectName, name, phaseNumber) VALUES (?, ?, ?, ?)", (project_id, project_name, name, phase_number))
        conn.commit()

    def read_cells(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cells")
        return cursor.fetchall()
    
    def read_single_cell(self, cell_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cells WHERE cell_id = ?", (cell_id,))
        return cursor.fetchone()
    
    def get_last_cell_id(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT cell_id FROM cells ORDER BY cell_id DESC LIMIT 1")
        return cursor.fetchone()[0]

    def delete_cell(self, cell_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cells WHERE cell_id = ?", (cell_id,))
        conn.commit()

    def create_cell_phase(self, cell_id, phase_number, area_mm2, perimeter_mm, diameter_mm, roundness, aspect_ratio, solidity, convexity, particle_count, scale_value, viability):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cellPhases (cell_id, phaseNumber, area_mm2, perimeter_mm, diameter_mm, roundness, aspectRatio, solidity, convexity, particleCount, scaleValue, viability) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (cell_id, phase_number, area_mm2, perimeter_mm, diameter_mm, roundness, aspect_ratio ,solidity, convexity, particle_count, scale_value, viability))
        conn.commit()

    def read_cell_phases(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cellPhases")
        return cursor.fetchall()
    
    def read_single_cell_phases(self, cell_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cellPhases WHERE cell_id = ?", (cell_id,))
        return cursor.fetchall()

    def delete_cell_phase(self, phase_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cellPhases WHERE phase_id = ?", (phase_id,))
        conn.commit()
        
    def get_cells_by_project_name(self, project_name):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cells WHERE projectName = ?", (project_name,))
        cells = cursor.fetchall()
        project_cells = []
        for cell in cells:
            cursor.execute("SELECT * FROM cellPhases WHERE cell_id = ?", (cell[0],))
            phases = cursor.fetchall()
            cell_phases = []
            for phase in phases:
                cell_phases.append({
                    "phase_number": phase[2],
                    "area_mm2": phase[3],
                    "perimeter_mm": phase[4],
                    "diameter_mm": phase[5],
                    "roundness": phase[6],
                    "aspect_ratio": phase[7],
                    "solidity": phase[8],
                    "convexity": phase[9],
                    "particle_count": phase[10],
                    "scale_value": phase[11],
                    "viability": phase[12]
                })
            project_cells.append(cell_phases)
        return project_cells