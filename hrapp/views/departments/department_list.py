import sqlite3
from django.shortcuts import render
from hrapp.models import Department
from hrapp.views.connection import Connection


def department_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                select d.id,
                    d.name,
                    d.budget,
                    COUNT(e.id) as employee_count
                FROM hrapp_department d
                    JOIN hrapp_employee e ON d.id = e.department_id
                GROUP BY d.name;
            """)

            all_departments = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                department = Department()
                department.id = row['id']
                department.name = row['name']
                department.budget = row['budget']
                department.employee_count = row['employee_count']

                all_departments.append(department)

    template = 'departments/departments_list.html'
    context = {
        'departments': all_departments
    }

    return render(request, template, context)
