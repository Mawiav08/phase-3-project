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
