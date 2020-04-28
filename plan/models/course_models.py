from djongo import models
from .expression_models import Expression
from .section_models import Section
from .utils_models import CourseCode

class UVicCourseDetails(models.Model):
    hours_lectures = models.DecimalField(max_digits=4, decimal_places=2)
    hours_labs = models.DecimalField(max_digits=4, decimal_places=2)
    hours_tutorials = models.DecimalField(max_digits=4, decimal_places=2)

class Course(models.Model):
    course_code = models.EmbeddedField(
        model_container = CourseCode
    )
    name = models.CharField(max_length=200)
    credits = models.DecimalField(max_digits=3, decimal_places=1)
    course_details = models.EmbeddedField(
        model_container = UVicCourseDetails
    )
    requirement = models.ArrayField(
        model_container = Expression
    )

class OfferingCourse(Course):
    sections = models.ArrayField(
        model_container = Section
    )
