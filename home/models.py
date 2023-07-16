import datetime
from django.db import models
from django.utils import timezone

class Problem(models.Model):
    problem_name=models.CharField(max_length=200)
    problem_statement=models.CharField(max_length=2000)
    def __str__(self):
        return self.problem_name