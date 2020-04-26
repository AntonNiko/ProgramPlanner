from .utils_models import *
from djongo import models

class Expression(models.Model):
    class Meta:
        abstract = True

class CourseExpression(Expression):
    course_code = models.EmbeddedField(
        model_container = CourseCode
    )
    requisite_type = models.CharField(
        max_length = 2,
        choices = [
            ('P', 'prerequisite'),
            ('C', 'corequisite')
        ]
    )

class ConditionalExpression(Expression):
    expression_one = models.EmbeddedField(
        model_container = Expression
    )
    expression_two = models.EmbeddedField(
        model_container = Expression
    )
    condition = models.CharField(
        max_length = 3,
        choices = [
            ('AND', 'AND'),
            ('OR', 'OR')
        ]
    )

class ListExpression(Expression):
    threshold = models.IntegerField()
    threshold_type = models.CharField(
        max_length = 3,
        choices = [
            ('LT', 'Less than'),
            ('LEQ', 'Less than or equal to'),
            ('EQ', 'Equal to'),
            ('GEQ', 'Greater than or equal to'),
            ('GT', 'Greater than')
        ]
    )
    expressions = models.ArrayField(
        model_container = Expression
    )

class RegistrationRestrictionExpression(Expression):
    expression = models.ArrayField(
        model_container = Expression
    )

class YearStandingExpression(Expression):
    threshold = models.IntegerField()
    threshold_type = models.CharField(
        max_length = 3,
        choices = [
            ('LT', 'Less than'),
            ('LEQ', 'Less than or equal to'),
            ('EQ', 'Equal to'),
            ('GEQ', 'Greater than or equal to'),
            ('GT', 'Greater than')
        ]
    )

class UnitsExpression(Expression):
    threshold = models.IntegerField()
    threshold_type = models.CharField(
        max_length = 3,
        choices = [
            ('LT', 'Less than'),
            ('LEQ', 'Less than or equal to'),
            ('EQ', 'Equal to'),
            ('GEQ', 'Greater than or equal to'),
            ('GT', 'Greater than')
        ]
    )
    expressions = models.ArrayField(
        model_container = Expression
    )