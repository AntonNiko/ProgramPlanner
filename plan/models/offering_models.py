from djongo import models
from .course_models import Course
from .schedule_models import Section


class CourseOffering(Course):
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



