from djongo import models
from plan.fields import MongoDecimalField
from .expression_models import Expression
from .section_models import Section
from .utils_models import CourseCode

class UVicCourseDetails(models.Model): 
    hours_lectures = MongoDecimalField(max_digits=4, decimal_places=2)
    hours_labs = MongoDecimalField(max_digits=4, decimal_places=2)
    hours_tutorials = MongoDecimalField(max_digits=4, decimal_places=2)

    def to_dict(self):
        result = {
            'hours_lectures': float(self.hours_lectures),
            'hours_labs': float(self.hours_labs),
            'hours_tutorials': float(self.hours_tutorials)
        }
        return result

class Course(models.Model):
    course_code = models.EmbeddedField(
        model_container = CourseCode
    )
    name = models.CharField(max_length=200)
    credits = MongoDecimalField(max_digits=3, decimal_places=1)
    course_details = models.EmbeddedField(
        model_container = UVicCourseDetails
    )
    requirement = models.ArrayField(
        model_container = Expression
    )

    def evaluate_requirement(self, sequence):
        pass

    def to_dict(self):
        result = {
            'course_code': self.course_code.to_dict(),
            'name': self.name,
            'credits': self.credits,
            'course_details': self.course_details.to_dict(),
            'requirement': [expression.to_dict() for expression in self.requirement]
        }
        return result

class OfferingCourse(Course):
    sections = models.ArrayField(
        model_container = Section
    )
