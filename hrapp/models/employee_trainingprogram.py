from django.db import models


class EmployeeTrainingProgram(models.Model):
    """
    Creates the join table for the many to many relationship between employees and training programs
    Author: Bryan Nilsen
    methods: none
    """

    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    trainingprogram = models.ForeignKey(
        "TrainingProgram", on_delete=models.CASCADE)
