import sqlite3

class DatabaseSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = sqlite3.connect("con.db")
        return cls._instance
    
    def __init__(self):
        self.create_tables_if_not_exist()

    # TODO: Add related constraints..
    def create_tables_if_not_exist(self):
        tables = {
            "projects": """
                CREATE TABLE IF NOT EXISTS projects (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    owner VARCHAR(255),
                    desc TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """,
            "cells": """
                CREATE TABLE IF NOT EXISTS cells (
                    cell_id INT, 
                    project_id INTEGER,
                    phase INT,
                    image_name VARCHAR(255),
                    area_mm2 REAL,
                    perimeter_mm REAL,
                    diameter_mm REAL,
                    class INTEGER, 
                    PRIMARY KEY (cell_id, phase),           
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                );
            """,
            
        }

        cursor = self.connection.cursor()
        for table_name, create_table_query in tables.items():
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            table_exists = cursor.fetchone()
            if not table_exists:
                cursor.execute(create_table_query)
                self.connection.commit()

    def get_connection(self):
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None