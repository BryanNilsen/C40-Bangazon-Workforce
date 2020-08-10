import sqlite3
from django.shortcuts import render
from hrapp.models import Employee, Department, Computer
from ..connection import Connection


def employee_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # TODO: Add to query: e.department,
            db_cursor.execute("""
                select e.id,
                    e.first_name,
                    e.last_name,
                    e.start_date,
                    e.is_supervisor,
                    d.id as department_id,
                    d.name as department_name,
                    c.id as computer_id,
                    c.make as computer_make
                from hrapp_employee e
                    join hrapp_department d on e.department_id = d.id
                    join hrapp_employeecomputer ec on e.id = ec.employee_id
                    join hrapp_computer c on ec.computer_id = c.id;
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
