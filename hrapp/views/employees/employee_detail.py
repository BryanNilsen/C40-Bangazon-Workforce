import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Employee, TrainingProgram
from hrapp.views.connection import Connection


def get_employee(employee_id):
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
                c.make AS computer_make,
                tp.title AS training_title,
                tp.id AS training_id
            FROM hrapp_employee e
                LEFT JOIN hrapp_department d ON e.department_id = d.id
                LEFT JOIN hrapp_employeecomputer ec ON e.id = ec.employee_id
                LEFT JOIN hrapp_computer c ON ec.computer_id = c.id
                LEFT JOIN hrapp_employeetrainingprogram etp ON etp.employee_id = e.id
                LEFT JOIN hrapp_trainingprogram tp ON etp.trainingprogram_id = tp.id
            WHERE ec.unassign_date ISNULL
                AND e.id = ?;
        """, (employee_id,))

        dataset = db_cursor.fetchall()

        employee = Employee()
        employee.id = dataset[0]['id']
        employee.first_name = dataset[0]['first_name']
        employee.last_name = dataset[0]['last_name']
        employee.is_supervisor = dataset[0]['is_supervisor']
        employee.department_id = dataset[0]['department_id']
        employee.department_name = dataset[0]['department_name']
        employee.computer_id = dataset[0]['computer_id']
        employee.computer_make = dataset[0]['computer_make']

        employee.trainingprograms = []

        for row in dataset:
            if row['training_id'] is not None:
                traininingprogram = TrainingProgram()
                traininingprogram.id = row['training_id']
                traininingprogram.title = row['training_title']
                employee.trainingprograms.append(traininingprogram)

        return employee


@login_required
def employee_details(request, employee_id):
    if request.method == 'GET':
        employee = get_employee(employee_id)
        template_name = 'employees/employee_detail.html'
        context = {
            'employee': employee
        }
        return render(request, template_name, context)
