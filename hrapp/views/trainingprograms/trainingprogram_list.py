import sqlite3
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from hrapp.models import TrainingProgram
from hrapp.views.connection import Connection
import datetime


def trainingprogram_list(request):
    '''
    This method checks request to define behavior
    If GET, this method gets all of the training programs that have not taken place yet, combines them with the trainingprogram_list template and sends the rendered html back in the response
    If POST, this method will take in the form data from the trainingprogram_form template, insert a new record into the database, and rerender the list of training programs
    '''
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            # gets programs that haven't started yet
            db_cursor.execute("""
                select t.id,
                    t.title,
                    t.start_date,
                    t.end_date,
                    t.capacity
                from hrapp_trainingprogram t
                where t.start_date >= DATETIME('now');
            """)

            all_trainingprograms = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                trainingprogram = TrainingProgram()
                trainingprogram.id = row['id']
                trainingprogram.title = row['title']
                # takes string datetime from db and converts to datetime object
                trainingprogram.start_date = datetime.datetime.strptime(
                    row['start_date'], "%Y-%m-%d %H:%M:%S")

                trainingprogram.end_date = datetime.datetime.strptime(
                    row['end_date'], "%Y-%m-%d %H:%M:%S")
                trainingprogram.capacity = row['capacity']

                all_trainingprograms.append(trainingprogram)

        template = 'trainingprograms/trainingprograms_list.html'
        context = {
            'trainingprograms': all_trainingprograms
        }

        return render(request, template, context)

    # HANDLE POST REQUEST
    if request.method == 'POST':
        form_data = request.POST
        start = form_data['start_date'].replace("T", " ") + ":00"
        end = form_data['end_date'].replace("T", " ") + ":00"

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_trainingprogram
            (
                title, start_date,
                end_date, capacity
            )
            VALUES (?, ?, ?, ?)
            """, (form_data['title'], start, end, form_data["capacity"]))

        return redirect(reverse('hrapp:trainingprogram_list'))
