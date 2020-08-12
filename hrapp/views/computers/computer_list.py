import sqlite3
from datetime import date
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from hrapp.models import Computer
from hrapp.views.connection import Connection


def computer_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT c.id,
                    c.make,
                    c.purchase_date,
                    c.decommission_date,
                    e.first_name || ' ' || e.last_name as fullname,
                    e.id as employee_id,
                    ec.assign_date
                FROM hrapp_computer c
                    LEFT JOIN hrapp_employeecomputer ec on ec.computer_id = c.id
                    LEFT JOIN hrapp_employee e on ec.employee_id = e.id
                WHERE ec.unassign_date ISNULL;
            """)

            all_computers = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                computer = Computer()
                computer.id = row['id']
                computer.make = row['make']
                computer.purchase_date = row['purchase_date']
                computer.decommission_date = row['decommission_date']
                computer.current_employee = row['fullname']
                computer.employee_id = row['employee_id']
                computer.assign_date = row['assign_date']

                all_computers.append(computer)

        template = 'computers/computer_list.html'
        context = {
            'computers': all_computers
        }

        return render(request, template, context)

    # HANDLE POST REQUEST
    if request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_computer
            (
                make, purchase_date
            )
            VALUES (?, ?)
            """, (form_data['make'], form_data['purchase_date']))

            # if employee is assigned to computer, make join table record
            if form_data['employee_id'] != "0":
                computer_id = db_cursor.lastrowid
                db_cursor.execute("""
                INSERT INTO hrapp_employeecomputer
                (
                    computer_id, employee_id, assign_date
                )
                VALUES(?, ?, ?)
                """,  (computer_id, form_data['employee_id'], date.today()))

        return redirect(reverse('hrapp:computer_list'))
