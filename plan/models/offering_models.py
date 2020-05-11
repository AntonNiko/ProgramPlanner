from djongo import models
from .course_models import Course
from .schedule_models import Section


class CourseOffering(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    term_type = models.PositiveSmallIntegerField(
        choices=[
            (1, 'spring'),
            (2, 'summer'),
            (3, 'fall')
        ]
    )
    sections = models.ArrayReferenceField(
        to=Section,
        on_delete=models.CASCADE
    )



