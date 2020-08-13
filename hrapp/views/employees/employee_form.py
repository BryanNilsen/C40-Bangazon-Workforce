import sqlite3
from hrapp.views.connection import Connection
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import Department, Employee, Computer
from hrapp.models import model_factory


def get_departments():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Department)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            d.id,
            d.name,
            d.budget
        from hrapp_department d
        """)

        return db_cursor.fetchall()


def get_computers():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Computer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                c.id,
                c.make,
                c.purchase_date,
                c.decommission_date
            FROM hrapp_computer c
            WHERE c.decommission_date ISNULL;
        """)

        return db_cursor.fetchall()


@login_required
def employee_form(request):
    if request.method == 'GET':
        departments = get_departments()
        template = 'employees/employee_form.html'
        context = {
            'all_departments': departments
        }

        return render(request, template, context)


@login_required
def employee_edit_form(request, employee_id):

    # TODO GET EMPLOYEE METHOD!!
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
                WHERE ec.unassign_date ISNULL
                    AND e.id = ?;
            """, (employee_id,))

            dataset = db_cursor.fetchone()

            employee = Employee()
            employee.id = dataset['id']
            employee.first_name = dataset['first_name']
            employee.start_date = dataset['start_date']
            employee.last_name = dataset['last_name']
            employee.is_supervisor = dataset['is_supervisor']
            employee.department_id = dataset['department_id']
            employee.department_name = dataset['department_name']
            employee.computer_id = dataset['computer_id']
            employee.computer_make = dataset['computer_make']

            computers = get_computers()
            departments = get_departments()

            template = 'employees/employee_form.html'
            context = {
                'employee': employee,
                'all_departments': departments,
                'all_computers': computers
            }

            return render(request, template, context)
