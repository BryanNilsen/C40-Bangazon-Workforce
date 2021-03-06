from django.urls import path
from django.conf.urls import include
from hrapp import views
from .views import *

app_name = 'hrapp'
urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls'), name='login'),
    path('logout/', logout_user, name='logout'),
    path('employees/', employee_list, name='employee_list'),
    path('employees/form', employee_form, name='employee_form'),
    path('employees/<int:employee_id>', employee_details, name='employee'),
    path('employees/<int:employee_id>/form/',
         employee_edit_form, name='employee_edit_form'),
    path('departments/', department_list, name='department_list'),
    path('departments/form', department_form, name='department_form'),
    path('departments/<int:department_id>/',
         department_details, name='department'),
    path('computers/', computer_list, name='computer_list'),
    path('computers/<int:computer_id>/', computer_details, name='computer'),
    path('computer/delete/<int:computer_id>/',
         delete_computer, name='computer_delete'),
    path('computers/form', computer_form, name='computer_form'),
    path('trainingprograms/', trainingprogram_list, name='trainingprogram_list'),
    path('trainingprograms/past', trainingprogram_past,
         name='trainingprogram_past'),
    path('trainingprograms/form', trainingprogram_form,
         name='trainingprogram_form')
]
