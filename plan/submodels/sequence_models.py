from django.contrib.auth.models import User
from djongo import models
from .course_models import *

class Term(models.Model):
    year = models.PositiveSmallIntegerField()
    term_type = models.PositiveSmallIntegerField(
        choices = [
            (1, 'Spring Term'),
            (2, 'Summer Term'),
            (3, 'Fall Term')
        ]
    )
    courses = models.ArrayField(
        model_container = Course
    )

class Sequence(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    terms = models.ArrayField(
        model_container = Term
    )