import sqlite3
from hrapp.views.connection import Connection
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def trainingprogram_form(request):
    if request.method == 'GET':
        template = 'trainingprograms/trainingprograms_form.html'
        context = {
            'trainingprogram': {}
        }

        return render(request, template, context)
