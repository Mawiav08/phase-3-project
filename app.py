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

class Employee:
    def __init__(self, db):
        self.db = db

    def add(self, name, age, position, department_id):
        query = "INSERT INTO employees_table (employee_name, employee_age, employee_position, department_id) VALUES (?, ?, ?, ?)"
        self.db.cursor.execute(query, (name, age, position, department_id))
        self.db.conn.commit()
        print(f"Employee {name} added successfully.")

    def remove(self, employee_id):
        query = "DELETE FROM employees_table WHERE employee_id = ?"
        self.db.cursor.execute(query, (employee_id,))
        self.db.conn.commit()
        print(f"Employee with ID {employee_id} removed successfully.")

    def promote(self, employee_id, new_position, new_salary, effective_date):
        update_position_query = "UPDATE employees_table SET employee_position = ? WHERE employee_id = ?"
        self.db.cursor.execute(update_position_query, (new_position, employee_id))
        
        add_salary_query = "INSERT INTO salaries_table (employee_id, salary_amount, effective_date) VALUES (?, ?, ?)"
        self.db.cursor.execute(add_salary_query, (employee_id, new_salary, effective_date))
        
        self.db.conn.commit()
        print(f"Employee with ID {employee_id} promoted to {new_position} with salary {new_salary} effective from {effective_date}.")

    def add_or_update_salary(self, employee_id, salary_amount, effective_date):
        self.db.cursor.execute("SELECT * FROM salaries_table WHERE employee_id = ? AND effective_date = ?", (employee_id, effective_date))
        record = self.db.cursor.fetchone()
        
        if record:
            update_salary_query = "UPDATE salaries_table SET salary_amount = ? WHERE employee_id = ? AND effective_date = ?"
            self.db.cursor.execute(update_salary_query, (salary_amount, employee_id, effective_date))
            print(f"Salary updated for employee ID {employee_id} on {effective_date}.")
        else:
            add_salary_query = "INSERT INTO salaries_table (employee_id, salary_amount, effective_date) VALUES (?, ?, ?)"
            self.db.cursor.execute(add_salary_query, (employee_id, salary_amount, effective_date))
            print(f"New salary record added for employee ID {employee_id}.")
        
        self.db.conn.commit()

    def display_salary_history(self, employee_id):
        query = "SELECT salary_amount, effective_date FROM salaries_table WHERE employee_id = ? ORDER BY effective_date"
        self.db.cursor.execute(query, (employee_id,))
        rows = self.db.cursor.fetchall()
        if rows:
            print(f"Salary history for employee ID {employee_id}:")
            for row in rows:
                print(f"Salary: {row[0]}, Effective Date: {row[1]}")
        else:
            print(f"No salary records found for employee ID {employee_id}.")

    def display(self):
        query = """
        SELECT e.employee_id, e.employee_name, e.employee_age, e.employee_position, d.department_name, s.salary_amount, s.effective_date
        FROM employees_table e
        JOIN departments_table d ON e.department_id = d.department_id
        LEFT JOIN (
            SELECT employee_id, salary_amount, effective_date
            FROM salaries_table
            WHERE (employee_id, effective_date) IN (
                SELECT employee_id, MAX(effective_date)
                FROM salaries_table
                GROUP BY employee_id
            )
        ) s ON e.employee_id = s.employee_id
        """
        self.db.cursor.execute(query)
        rows = self.db.cursor.fetchall()
        if rows:
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Position: {row[3]}, Department: {row[4]}, Salary: {row[5]}, Effective Date: {row[6]}")
        else:
            print("No employees found.")

class EmployeeManagementSystem:
    def __init__(self):
        self.db = Database()
        self.department = Department(self.db)
        self.employee = Employee(self.db)
        self.department.populate_default_departments()

    def run(self):
        while True:
            print("\nEmployee Management System")
            print("1. Add Employee")
            print("2. Remove Employee")
            print("3. Promote Employee")
            print("4. Display Employees")
            print("5. Add Department")
            print("6. Display Departments")
            print("7. Add/Update Salary")
            print("8. Display Salary History")
            print("9. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                name = input("Enter name: ")
                age = int(input("Enter age: "))
                position = input("Enter position: ")
                department_id = int(input("Enter department ID: "))
                self.employee.add(name, age, position, department_id)
            elif choice == '2':
                employee_id = int(input("Enter employee ID to remove: "))
                self.employee.remove(employee_id)
            elif choice == '3':
                employee_id = int(input("Enter employee ID to promote: "))
                new_position = input("Enter new position: ")
                new_salary = float(input("Enter new salary: "))
                effective_date = input("Enter effective date (YYYY-MM-DD): ")
                self.employee.promote(employee_id, new_position, new_salary, effective_date)
            elif choice == '4':
                self.employee.display()
            elif choice == '5':
                department_name = input("Enter department name: ")
                location = input("Enter location: ")
                self.department.add(department_name, location)
            elif choice == '6':
                self.department.display()
            elif choice == '7':
                employee_id = int(input("Enter employee ID: "))
                salary_amount = float(input("Enter salary amount: "))
                effective_date = input("Enter effective date (YYYY-MM-DD): ")
                self.employee.add_or_update_salary(employee_id, salary_amount, effective_date)
            elif choice == '8':
                employee_id = int(input("Enter employee ID to display salary history: "))
                self.employee.display_salary_history(employee_id)
            elif choice == '9':
                self.db.close()
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    system = EmployeeManagementSystem()
    system.run()
