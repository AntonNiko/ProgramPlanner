from djongo import models
from plan.expressions import *
from plan.fields import MongoDecimalField
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
        model_container=CourseCode,
        blank=False
    )
    name = models.CharField(max_length=200)
    credits = MongoDecimalField(max_digits=3, decimal_places=1)
    course_details = models.EmbeddedField(
        model_container=UVicCourseDetails,
        blank=False
    )
    requirement = models.DictField(default={'expressions': []}, blank=False)

    def evaluate_requirement(self, sequence):
        """
        Evaluates if the requirement is satisfied given a sequence.
        """

        expressions = [ExpressionFactory.build_and_get_expression(json_data) for json_data in
                       self.requirement['expressions']]

        evaluation_result_container = []
        evaluation_result_status = True

        for expression in expressions:
            result = expression.evaluate_expression(sequence)
            evaluation_result_container.append(result.expression_status)
            if not result.satisfied:
                evaluation_result_status = False
                break

        return evaluation_result_status, evaluation_result_container

    def to_dict(self):
        result = {
            'course_code': self.course_code.to_dict(),
            'name': self.name,
            'credits': self.credits,
            'course_details': self.course_details.to_dict(),
            'requirement': self.requirement
        }
        return result
