import sqlite3
from hrapp.views.connection import Connection
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer
from hrapp.models import Employee
from hrapp.models import model_factory


def get_employees():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Employee)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            e.id,
            e.first_name,
            e.last_name
        from hrapp_employee e
        """)

        return db_cursor.fetchall()


@login_required
def computer_form(request):
    if request.method == 'GET':
        employees = get_employees()
        template = 'computers/computer_form.html'
        context = {
            'all_employees': employees
        }

        return render(request, template, context)
