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

    def update_project(self, project_id, name, owner):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE projects SET name = ?, owner = ? , desc = ? WHERE id = ?", (name, owner, project_id))
        conn.commit()

    def delete_project(self, project_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()

    def create_cell(self, project_id, image_name, area_mm2, perimeter_mm, diameter_mm, class_):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cells (project_id, image_name, area_mm2, perimeter_mm, diameter_mm, class) VALUES (?, ?, ?, ?, ?, ?)", (project_id, image_name, area_mm2, perimeter_mm, diameter_mm, class_))
        conn.commit()

    def read_cells(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cells")
        return cursor.fetchall()

    def update_cell(self, cell_id, project_id, image_name, area_mm2, perimeter_mm, diameter_mm, class_):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE cells SET project_id = ?, image_name = ?, area_mm2 = ?, perimeter_mm = ?, diameter_mm = ?, class = ? WHERE id = ?", (project_id, image_name, area_mm2, perimeter_mm, diameter_mm, class_, cell_id))
        conn.commit()

    def delete_cell(self, cell_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cells WHERE id = ?", (cell_id,))
        conn.commit()