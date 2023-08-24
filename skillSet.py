import datetime
import mysql.connector
import tkinter as tk
from tkinter import ttk

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='W@2915djkq#',
    database='employeeSkillSet'
)

# Create a cursor
cursor = conn.cursor()

# Create the main tkinter window
root = tk.Tk()
root.title("EMPLOYEE SKILL INVENTORY MANAGEMENT")

# Create and execute the table creation SQL
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employee (
        emp_id INT PRIMARY KEY,
        emp_name VARCHAR(255),
        emp_salary INT,
        emp_specialization VARCHAR(255),
        emp_hireDate DATE,
        emp_projectStatus ENUM('P', 'N') DEFAULT 'N'
    )
''')
conn.commit()

# GUI functions
def add_emp():
    emp_id = emp_id_entry.get()
    emp_name = emp_name_entry.get()
    emp_salary = emp_salary_entry.get()
    emp_specialization = emp_specialization_entry.get()
    emp_hireDate = emp_hireDate_entry.get()

    try:
        emp_id = int(emp_id)
        emp_salary = int(emp_salary)
        hire_date = datetime.date.fromisoformat(emp_hireDate)
    except ValueError:
        result_label.config(text="Invalid input. Please check your input values.")
        return

    cursor.execute('''
        INSERT INTO employee (emp_id, emp_name, emp_salary, emp_specialization, emp_hireDate) 
        VALUES (%s, %s, %s, %s, %s)
    ''', (emp_id, emp_name, emp_salary, emp_specialization, hire_date))
    conn.commit()
    result_label.config(text="Employee added successfully!")

def view_items():
    cursor.execute('SELECT * FROM employee')
    employees = cursor.fetchall()

    if not employees:
        result_label.config(text="No employees in the database.")
    else:
        result_label.config(text="")
        for employee in employees:
            result_label.config(text=result_label.cget("text") +
                                        f"ID: {employee[0]}, NAME: {employee[1]}, SALARY: {employee[2]}, HIRING DATE: {employee[3]}, SKILL SET: {employee[4]}, WORKING STATUS: {employee[5]}\n")

def remove_employee():
    emp_id = emp_id_entry.get()
    try:
        emp_id = int(emp_id)
    except ValueError:
        result_label.config(text="Invalid input. Please enter a valid Employee ID.")
        return

    cursor.execute('DELETE FROM employee WHERE emp_id = %s', (emp_id,))
    conn.commit()
    result_label.config(text="Employee removed successfully!")

def search_employee_by_id():
    emp_id = emp_id_entry.get()
    try:
        emp_id = int(emp_id)
    except ValueError:
        result_label.config(text="Invalid input. Please enter a valid Employee ID.")
        return

    cursor.execute('SELECT * FROM employee WHERE emp_id = %s', (emp_id,))
    employee = cursor.fetchone()

    if not employee:
        result_label.config(text="Employee not found.")
    else:
        result_label.config(text=f"ID: {employee[0]}, NAME: {employee[1]}, SALARY: {employee[2]}, HIRING DATE: {employee[3]}, SKILL SET: {employee[4]}, WORKING STATUS: {employee[5]}")

def search_employee_by_name():
    emp_name = emp_name_entry.get()
    cursor.execute('SELECT * FROM employee WHERE emp_name LIKE %s', ('%' + emp_name + '%',))
    employees = cursor.fetchall()

    if not employees:
        result_label.config(text="Employee not found.")
    else:
        result_label.config(text="")
        for employee in employees:
            result_label.config(text=result_label.cget("text") +
                                        f"ID: {employee[0]}, NAME: {employee[1]}, SALARY: {employee[2]}, HIRING DATE: {employee[3]}, SKILL SET: {employee[4]}, WORKING STATUS: {employee[5]}\n")

def update_project_status():
    emp_id = emp_id_entry.get()
    new_emp_projectStatus = new_emp_projectStatus_entry.get()
    try:
        emp_id = int(emp_id)
    except ValueError:
        result_label.config(text="Invalid input. Please enter a valid Employee ID.")
        return

    cursor.execute('UPDATE employee SET emp_projectStatus = %s WHERE emp_id = %s', (new_emp_projectStatus, emp_id))
    conn.commit()
    result_label.config(text="Project Status updated successfully!")

def project_requirement():
    emp_specialization = emp_specialization_entry.get()
    cursor.execute('SELECT * FROM employee WHERE emp_specialization LIKE %s AND emp_projectStatus = "N"', ('%' + emp_specialization + '%',))
    employees = cursor.fetchall()

    if not employees:
        result_label.config(text="No employees found for the project requirement.")
    else:
        result_label.config(text="")
        for employee in employees:
            result_label.config(text=result_label.cget("text") +
                                        f"ID: {employee[0]}, NAME: {employee[1]}, SALARY: {employee[2]}, HIRING DATE: {employee[3]}, SKILL SET: {employee[4]}, WORKING STATUS: {employee[5]}\n")
def clear_fields():
    emp_id_entry.delete(0, tk.END)
    emp_name_entry.delete(0, tk.END)
    emp_salary_entry.delete(0, tk.END)
    emp_specialization_entry.delete(0, tk.END)
    emp_hireDate_entry.delete(0, tk.END)
    new_emp_projectStatus_entry.delete(0, tk.END)
    result_label.config(text="")


# Create GUI elements
#root.geometry("500x400")
program_name= ttk.Label(root, text="EMPLOYEE DATABASE: ", font='Times 12 bold', justify="left" )
emp_id_label = ttk.Label(root, text="Employee ID:",font='Times 12')
emp_id_entry = ttk.Entry(root)

emp_name_label = ttk.Label(root, text="Employee Name:",font='Times 12')
emp_name_entry = ttk.Entry(root)

emp_salary_label = ttk.Label(root, text="Employee Salary:",font='Times 12')
emp_salary_entry = ttk.Entry(root)

emp_specialization_label = ttk.Label(root, text="Employee Specialization:",font='Times 12')
emp_specialization_entry = ttk.Entry(root)

emp_hireDate_label = ttk.Label(root, text="Employee Hire Date (YYYY-MM-DD):",font='Times 12')
emp_hireDate_entry = ttk.Entry(root)

add_button = ttk.Button(root, text="Add Employee", command=add_emp)

view_emps = ttk.Label(root, text="VIEW ALL EMPLOYEES: ", font='Times 12 bold')

view_button = ttk.Button(root, text="View Employees", command=view_items)

remove_emps = ttk.Label(root, text="REMOVE AN EMPLOYEE: ", font='Times 12 bold')
remove_button = ttk.Button(root, text="Remove Employee", command=remove_employee)

search_id = ttk.Label(root, text="SEARCH EMPLOYEE BY ID: ", font='Times 12 bold')
search_id_button = ttk.Button(root, text="Search Employee by ID", command=search_employee_by_id)

search_name = ttk.Label(root, text="SEARCH EMPLOYEE BY NAME: ", font='Times 12 bold')
search_name_button = ttk.Button(root, text="Search Employee by Name", command=search_employee_by_name)

proj_req= ttk.Label(root, text="WHAT ARE THE PROJECT REQUIREMENTS?: ", font='Times 12 bold')
project_requirement_button = ttk.Button(root, text="Project Requirement", command=project_requirement)

update_ps= ttk.Label(root, text="UPDATE PROJECT STATUS: ", font='Times 12 bold')
update_status_button = ttk.Button(root, text="Update Project Status", command=update_project_status)


new_emp_projectStatus_label = ttk.Label(root, text="New Project Status:")
new_emp_projectStatus_entry = ttk.Entry(root)

result_label = ttk.Label(root, text="", wraplength=400)

# Place GUI elements using grid layout manager
program_name.grid(row=0, column=0, pady=10)
emp_id_label.grid(row=1, column=0, pady=10)
emp_id_entry.grid(row=1, column=1,pady=10)

emp_name_label.grid(row=2, column=0,pady=10)
emp_name_entry.grid(row=2, column=1,pady=10)
emp_salary_label.grid(row=3, column=0,pady=10)
emp_salary_entry.grid(row=3, column=1,pady=10)
emp_specialization_label.grid(row=4, column=0,pady=10)
emp_specialization_entry.grid(row=4, column=1,pady=10)
emp_hireDate_label.grid(row=5, column=0,pady=10)
emp_hireDate_entry.grid(row=5, column=1,pady=10)

add_button.grid(row=5, column=3, columnspan=2, padx=5, pady=5)

view_emps.grid(row=7, column=0, pady=5)
view_button.grid(row=7, column=1, pady=5)

remove_emps.grid(row=9, column=0, pady=5)
remove_button.grid(row=9, column=1, pady=5)

search_id.grid(row=11, column=0, pady=5)
search_id_button.grid(row=11, column=1, pady=5)

search_name.grid(row=13, column=0, pady=5)
search_name_button.grid(row=13, column=1, pady=5)

proj_req.grid(row=15, column=0, pady=5)
project_requirement_button.grid(row=15, column=1, pady=5)

update_ps.grid(row=17, column=0, pady=5)
update_status_button.grid(row=17, column=1, pady=5)

new_emp_projectStatus_label.grid(row=19, column=0, pady=5)
new_emp_projectStatus_entry.grid(row=19, column=1, pady=5)

result_label.grid(row=22, column=0, columnspan=2, padx=5, pady=5)

# Create a button to clear fields
clear_button = ttk.Button(root, text="Clear Fields", command=clear_fields)
clear_button.grid(row=21, column=0, columnspan=2, padx=5, pady=5)

# Main loop
root.mainloop()
conn.close()
