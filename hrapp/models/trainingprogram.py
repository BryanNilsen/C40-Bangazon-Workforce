from django.db import models
from django.urls import reverse


class TrainingProgram(models.Model):

    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    capacity = models.IntegerField()

    class Meta:
        verbose_name = ("TrainingProgram")
        verbose_name_plural = ("TrainingPrograms")

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("TrainingProgram_detail", kwargs={"pk": self.pk})
