import sqlite3

class Database:
    def __init__(self, db_name="employees.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees_table (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            employee_age INTEGER NOT NULL,
            employee_position TEXT NOT NULL,
            department_id INTEGER NOT NULL,
            FOREIGN KEY (department_id) REFERENCES departments_table(department_id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments_table (
            department_id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_name TEXT NOT NULL,
            location TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS salaries_table (
            salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            salary_amount REAL NOT NULL,
            effective_date TEXT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees_table(employee_id)
        )
        """)

        self.conn.commit()

    def close(self):
        self.conn.close()
