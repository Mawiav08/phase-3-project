import sqlite3

def create_tables():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees_table (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_name TEXT NOT NULL,
        employee_age INTEGER NOT NULL,
        employee_position TEXT NOT NULL,
        department_id INTEGER NOT NULL,
        FOREIGN KEY (department_id) REFERENCES departments_table(department_id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments_table (
        department_id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT NOT NULL,
        location TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS salaries_table (
        salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        salary_amount REAL NOT NULL,
        effective_date TEXT NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees_table(employee_id)
    )
    """)
    
    conn.commit()
    conn.close()

def add_department(department_name, location):
    valid_departments = ['Finance', 'HR', 'Administration', 'Marketing', 'Accounting']
    if department_name not in valid_departments:
        print("Invalid department name. Please choose from: Finance, HR, Administration, Marketing, Accounting")
        return
    
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT department_name FROM departments_table WHERE department_name = ?", (department_name,))
    if cursor.fetchone() is None:
        query = "INSERT INTO departments_table (department_name, location) VALUES (?, ?)"
        cursor.execute(query, (department_name, location))
        conn.commit()
        print(f"Department {department_name} added successfully.")
    else:
        print(f"Department {department_name} already exists.")
    
    conn.close()

def add_employee(name, age, position, department_id):
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    query = "INSERT INTO employees_table (employee_name, employee_age, employee_position, department_id) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (name, age, position, department_id))
    conn.commit()
    conn.close()
    print(f"Employee {name} added successfully.")

def remove_employee(employee_id):
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    query = "DELETE FROM employees_table WHERE employee_id = ?"
    cursor.execute(query, (employee_id,))
    conn.commit()
    conn.close()
    print(f"Employee with ID {employee_id} removed successfully.")

def promote_employee(employee_id, new_position, new_salary, effective_date):
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    
    update_position_query = "UPDATE employees_table SET employee_position = ? WHERE employee_id = ?"
    cursor.execute(update_position_query, (new_position, employee_id))
    
    add_salary_query = "INSERT INTO salaries_table (employee_id, salary_amount, effective_date) VALUES (?, ?, ?)"
    cursor.execute(add_salary_query, (employee_id, new_salary, effective_date))
    
    conn.commit()
    conn.close()
    print(f"Employee with ID {employee_id} promoted to {new_position} with salary {new_salary} effective from {effective_date}.")

def add_or_update_salary(employee_id, salary_amount, effective_date):
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()

    # Check if there is already a salary record for the given date
    cursor.execute("SELECT * FROM salaries_table WHERE employee_id = ? AND effective_date = ?", (employee_id, effective_date))
    record = cursor.fetchone()
    
    if record:
        # Update existing salary record
        update_salary_query = "UPDATE salaries_table SET salary_amount = ? WHERE employee_id = ? AND effective_date = ?"
        cursor.execute(update_salary_query, (salary_amount, employee_id, effective_date))
        print(f"Salary updated for employee ID {employee_id} on {effective_date}.")
    else:
        # Insert new salary record
        add_salary_query = "INSERT INTO salaries_table (employee_id, salary_amount, effective_date) VALUES (?, ?, ?)"
        cursor.execute(add_salary_query, (employee_id, salary_amount, effective_date))
        print(f"New salary record added for employee ID {employee_id}.")

    conn.commit()
    conn.close()

def display_salary_history(employee_id):
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    query = "SELECT salary_amount, effective_date FROM salaries_table WHERE employee_id = ? ORDER BY effective_date"
    cursor.execute(query, (employee_id,))
    rows = cursor.fetchall()
    conn.close()
    if rows:
        print(f"Salary history for employee ID {employee_id}:")
        for row in rows:
            print(f"Salary: {row[0]}, Effective Date: {row[1]}")
    else:
        print(f"No salary records found for employee ID {employee_id}.")

def display_employees():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
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
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Position: {row[3]}, Department: {row[4]}, Salary: {row[5]}, Effective Date: {row[6]}")
    else:
        print("No employees found.")

def display_departments():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    query = "SELECT * FROM departments_table"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    if rows:
        for row in rows:
            print(f"Department ID: {row[0]}, Department Name: {row[1]}, Location: {row[2]}")
    else:
        print("No departments found.")

def populate_default_departments():
    default_departments = [
        ('Finance', 'Building A'),
        ('HR', 'Building B'),
        ('Administration', 'Building C'),
        ('Marketing', 'Building D'),
        ('Accounting', 'Building E')
    ]
    
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    
    for dept_name, location in default_departments:
        cursor.execute("SELECT department_name FROM departments_table WHERE department_name = ?", (dept_name,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO departments_table (department_name, location) VALUES (?, ?)", (dept_name, location))
            print(f"Inserted department: {dept_name}, Location: {location}")
        else:
            print(f"Department {dept_name} already exists in the database.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    populate_default_departments()
    
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
            add_employee(name, age, position, department_id)
        elif choice == '2':
            employee_id = int(input("Enter employee ID to remove: "))
            remove_employee(employee_id)
        elif choice == '3':
            employee_id = int(input("Enter employee ID to promote: "))
            new_position = input("Enter new position: ")
            new_salary = float(input("Enter new salary: "))
            effective_date = input("Enter effective date (YYYY-MM-DD): ")
            promote_employee(employee_id, new_position, new_salary, effective_date)
        elif choice == '4':
            display_employees()
        elif choice == '5':
            department_name = input("Enter department name: ")
            location = input("Enter location: ")
            add_department(department_name, location)
        elif choice == '6':
            display_departments()
        elif choice == '7':
            employee_id = int(input("Enter employee ID: "))
            salary_amount = float(input("Enter salary amount: "))
            effective_date = input("Enter effective date (YYYY-MM-DD): ")
            add_or_update_salary(employee_id, salary_amount, effective_date)
        elif choice == '8':
            employee_id = int(input("Enter employee ID to display salary history: "))
            display_salary_history(employee_id)
        elif choice == '9':
            break
        else:
            print("Invalid choice, please try again.")
