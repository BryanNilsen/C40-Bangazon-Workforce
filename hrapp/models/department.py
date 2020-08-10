from django.db import models
from django.urls import reverse


class Department(models.Model):

    name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        verbose_name = ("Department")
        verbose_name_plural = ("Departments")

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("Department_detail", kwargs={"pk": self.pk})
