class Department:
    valid_departments = ['Finance', 'HR', 'Administration', 'Marketing', 'Accounting']

    def __init__(self, db):
        self.db = db

    def add(self, department_name, location):
        if department_name not in self.valid_departments:
            print("Invalid department name. Please choose from: Finance, HR, Administration, Marketing, Accounting")
            return
        
        self.db.cursor.execute("SELECT department_name FROM departments_table WHERE department_name = ?", (department_name,))
        if self.db.cursor.fetchone() is None:
            query = "INSERT INTO departments_table (department_name, location) VALUES (?, ?)"
            self.db.cursor.execute(query, (department_name, location))
            self.db.conn.commit()
            print(f"Department {department_name} added successfully.")
        else:
            print(f"Department {department_name} already exists.")

    def display(self):
        self.db.cursor.execute("SELECT * FROM departments_table")
        rows = self.db.cursor.fetchall()
        if rows:
            for row in rows:
                print(f"Department ID: {row[0]}, Department Name: {row[1]}, Location: {row[2]}")
        else:
            print("No departments found.")

    def populate_default_departments(self):
        default_departments = [
            ('Finance', 'Building A'),
            ('HR', 'Building B'),
            ('Administration', 'Building C'),
            ('Marketing', 'Building D'),
            ('Accounting', 'Building E')
        ]
        
        for dept_name, location in default_departments:
            self.db.cursor.execute("SELECT department_name FROM departments_table WHERE department_name = ?", (dept_name,))
            if self.db.cursor.fetchone() is None:
                self.db.cursor.execute("INSERT INTO departments_table (department_name, location) VALUES (?, ?)", (dept_name, location))
                print(f"Inserted department: {dept_name}, Location: {location}")
            else:
                print(f"Department {dept_name} already exists in the database.")
        
        self.db.conn.commit()
