from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from djongo import models
from .course_models import Course

class Term(models.Model):
    year = models.PositiveSmallIntegerField()
    term_type = models.PositiveSmallIntegerField(
        choices = [
            (1, 'spring'),
            (2, 'summer'),
            (3, 'fall')
        ]
    )
    courses = models.ArrayField(
        model_container = Course,
        blank = False
    )

    def to_dict(self):
        result = {
            'year': self.year,
            'term_type': self.term_type,
            'courses': [course.to_dict() for course in self.courses]
        }
        return result

class Sequence(models.Model):
    terms = models.ArrayField(
        model_container = Term
    )

    def to_dict(self):
        result = {
            'terms': [term.to_dict() for term in self.terms]
        }
        return result