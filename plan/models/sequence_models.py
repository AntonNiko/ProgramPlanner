from django.contrib.auth.models import User
from djongo import models
from .course_models import Course


class Term(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    term_type = models.PositiveSmallIntegerField(
        choices=[
            (1, 'spring'),
            (2, 'summer'),
            (3, 'fall')
        ]
    )
    courses = models.ArrayReferenceField(
        to=Course,
        on_delete=models.CASCADE
    )

    def to_dict(self):
        result = {
            'year': self.year,
            'term_type': self.term_type,
            'courses': [course.to_dict() for course in self.courses.all()]
        }
        return result

    def __gt__(self, other):
        return True if (self.year, self.term_type) > (other.year, other.term_type) else False

    def __ge__(self, other):
        return True if (self.year, self.term_type) >= (other.year, other.term_type) else False


class Sequence(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    terms = models.ArrayReferenceField(
        to=Term,
        on_delete=models.CASCADE
    )

    def to_dict(self):
        result = {
            'name': self.name,
            'terms': [term.to_dict() for term in self.terms.all()]
        }
        return result
