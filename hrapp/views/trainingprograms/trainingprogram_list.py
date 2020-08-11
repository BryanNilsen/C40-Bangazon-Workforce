import sqlite3
from django.shortcuts import render
from hrapp.models import TrainingProgram
from hrapp.views.connection import Connection
import datetime


def trainingprogram_list(request):
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
