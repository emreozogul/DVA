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

    def delete_project(self, project_name):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE name = ?", (project_name,))
        conn.commit()

    def create_cell(conn, cell_data):
        sql = ''' INSERT INTO cells(cell_id, project_id, phase, image_name, area_mm2, perimeter_mm, diameter_mm, class)
                VALUES(?,?,?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, cell_data)
        conn.commit()

    def read_cells(conn, cell_id=None):
        cur = conn.cursor()
        query = "SELECT * FROM cells"
        if cell_id:
            query += " WHERE cell_id=?"
            cur.execute(query, (cell_id,))
        else:
            cur.execute(query)
        rows = cur.fetchall()
        return rows
    
    def update_cell(conn, cell_data):
        sql = ''' UPDATE cells
                SET class = ?, image_name = ?
                WHERE cell_id = ? AND phase = ?'''
        cur = conn.cursor()
        cur.execute(sql, cell_data)
        conn.commit()

    def delete_cell(self, cell_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cells WHERE id = ?", (cell_id,))
        conn.commit()