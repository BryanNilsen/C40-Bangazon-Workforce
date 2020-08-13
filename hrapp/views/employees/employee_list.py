import sqlite3
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from hrapp.models import Employee, Department, Computer
from hrapp.views.connection import Connection


def employee_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT e.id,
                    e.first_name,
                    e.last_name,
                    e.start_date,
                    e.is_supervisor,
                    d.id AS department_id,
                    d.name AS department_name,
                    c.id AS computer_id,
                    c.make AS computer_make
                FROM hrapp_employee e
                    LEFT JOIN hrapp_department d ON e.department_id = d.id
                    LEFT JOIN hrapp_employeecomputer ec ON e.id = ec.employee_id
                    LEFT JOIN hrapp_computer c ON ec.computer_id = c.id
                WHERE ec.unassign_date ISNULL;
            """)

            all_employees = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                employee = Employee()
                employee.id = row['id']
                employee.first_name = row['first_name']
                employee.last_name = row['last_name']
                employee.start_date = row['start_date']
                employee.is_supervisor = row['is_supervisor']

                employee.department = Department()
                employee.department.id = row['department_id']
                employee.department.name = row['department_name']

                employee.computer = Computer()
                employee.computer.make = row['computer_make']

                all_employees.append(employee)

        template = 'employees/employees_list.html'
        context = {
            'employees': all_employees
        }

        return render(request, template, context)

    # HANDLE POST REQUEST
    if request.method == 'POST':
        form_data = request.POST
        is_supervisor = 0
        if 'is_supervisor' in form_data:
            is_supervisor = 1

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_employee
            (
                first_name, last_name, start_date,
                is_supervisor, department_id
            )
            VALUES (?, ?, ?, ?, ?)
            """, (form_data['first_name'], form_data['last_name'], form_data['start_date'], is_supervisor,  form_data["department_id"]))

        return redirect(reverse('hrapp:employee_list'))
