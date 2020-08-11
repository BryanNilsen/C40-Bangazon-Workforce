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

    # elif request.method == 'POST':
    #     form_data = request.POST

        # Check if this POST is for editing a book
        # if (
        #     "actual_method" in form_data
        #     and form_data["actual_method"] == "PUT"
        # ):
        #     with sqlite3.connect(Connection.db_path) as conn:
        #         db_cursor = conn.cursor()

        #         db_cursor.execute("""
        #         UPDATE libraryapp_book
        #         SET title = ?,
        #             author = ?,
        #             isbn = ?,
        #             year_published = ?,
        #             location_id = ?
        #         WHERE id = ?
        #         """, (
        #             form_data['title'], form_data['author'],
        #             form_data['isbn'], form_data['year_published'],
        #             form_data["location"], book_id,
        #         ))

        #     return redirect(reverse('libraryapp:books'))

        # Check if this POST is for deleting a book
        # if (
        #     "actual_method" in form_data
        #     and form_data["actual_method"] == "DELETE"
        # ):
        #     with sqlite3.connect(Connection.db_path) as conn:
        #         db_cursor = conn.cursor()

        #         db_cursor.execute("""
        #             DELETE FROM libraryapp_book
        #             WHERE id = ?
        #         """, (book_id,))

        #     return redirect(reverse('libraryapp:books'))
