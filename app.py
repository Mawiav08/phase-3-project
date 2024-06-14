from models.database import Database
from models.departments import Department
from models.employees import Employee

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
