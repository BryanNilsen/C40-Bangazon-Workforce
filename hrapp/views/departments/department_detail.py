import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Department, Employee
from hrapp.views.connection import Connection


def get_department(department_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT d.id,
                d.name,
                d.budget,
                e.first_name || ' ' || e.last_name AS fullname,
                e.id as employee_id
            FROM hrapp_department d
            LEFT JOIN hrapp_employee e ON e.department_id = d.id
            WHERE d.id = ?
        """, (department_id,))

        dataset = db_cursor.fetchall()
        
        department = Department()
        department.id = dataset[0]['id']
        department.name = dataset[0]['name']
        department.budget = dataset[0]['budget']

        department.employees = []

        for row in dataset:
            if row['fullname'] is not None:
                employee = Employee()
                employee.id = row['employee_id']
                employee.fullname = row['fullname']
                department.employees.append(employee)

        return department


@login_required
def department_details(request, department_id):
    if request.method == 'GET':
        department = get_department(department_id)
        template_name = 'departments/department_detail.html'
        context = {
            'department': department
        }
        return render(request, template_name, context)
