import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer
from hrapp.views.connection import Connection


def create_computer(cursor, row):
    _row = sqlite3.Row(cursor, row)

    computer = Computer()
    computer.id = _row["id"]
    computer.make = _row["make"]
    computer.purchase_date = _row["purchase_date"]
    computer.decommission_date = _row["decommission_date"]

    return computer


def get_computer(computer_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_computer
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT c.id,
            c.make,
            c.purchase_date,
            c.decommission_date
        FROM hrapp_computer c
        WHERE c.id = ?
        """, (computer_id,))

        return db_cursor.fetchone()


@login_required
def computer_details(request, computer_id):
    if request.method == 'GET':
        computer = get_computer(computer_id)
        template_name = 'computers/computer_detail.html'
        return render(request, template_name, {'computer': computer})

    if request.method == 'POST':
        form_data = request.POST
        # Check if this POST is for deleting a book
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM hrapp_computer
                    WHERE id = ?
                """, (computer_id,))

            return redirect(reverse('hrapp:computer_list'))


@login_required
def delete_computer(request, computer_id):

    if request.method == 'POST':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
            SELECT ec.id,
                ec.computer_id,
                c.make, c.purchase_date,
                c.decommission_date
            FROM hrapp_employeecomputer ec
            JOIN hrapp_computer c ON c.id = ec.computer_id
            WHERE ec.computer_id = ?
            """, (computer_id,))

            all_computers = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                computer = Computer()
                computer.id = row['id']
                computer.make = row['make']
                computer.purchase_date = row['purchase_date']
                computer.decommission_date = row['decommission_date']

                all_computers.append(computer)

            computer = get_computer(computer_id)
            can_delete = len(all_computers) == 0
            template = 'computers/computer_delete.html'
            context = {
                'computer': computer,
                'can_delete': can_delete
            }

            return render(request, template, context)
