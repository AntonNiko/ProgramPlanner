from .utils_models import CourseCode
from djongo import models



class ExpressionResultContainer():

    def __init__(self):
        self.satisifed = False
        self.expression_status = []
        
    def add_expression_status(self, message, satisfied):
        self.satisfied = satisfied

        if message == None:
            return 

        self.expression_status.append({
            'message': message,
            'satisfied': satisfied
        })


class Expression(models.Model):
    pass
    #class Meta:
    #    abstract = True


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

    @staticmethod
    def build_and_get_expression(json_data):
        course_code = CourseCode(subject=json_data['subject'], number=json_data['number'])
        requisite_type = json_data['requisite_type']
        return CourseExpression(course_code=course_code, requisite_type=requisite_type)

    def evaluate_expression(self, sequence, result_container=None):
        if result_container == None:
            result_container = ExpressionResultContainer()

        

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
            ('AND', 'and'),
            ('OR', 'or')
        ]
    )

    @staticmethod
    def build_and_get_expression(json_data):
        expression_one = ExpressionFactory.build_and_get_expression(json_data['expression_one'])
        expression_two = ExpressionFactory.build_and_get_expression(json_data['expression_two'])
        condition = json_data['condition']
        return ConditionalExpression(expression_one, expression_two, condition)

    def evaluate_expression(self, sequence, result_container=None):
        
        if result_container == None:
            result_container = ExpressionResultContainer()



class ListExpression(Expression):
    threshold_value = models.IntegerField()
    threshold_type = models.CharField(
        max_length = 3,
        choices = [
            ('LT', 'lt'),
            ('LEQ', 'lte'),
            ('EQ', 'eq'),
            ('GEQ', 'geq'),
            ('GT', 'gt')
        ]
    )
    expressions = models.ArrayField(
        model_container = Expression
    )

    @staticmethod
    def build_and_get_expression(json_data):
        threshold = json_data['threshold_value']
        threshold_type = json_data['threshold_type']
        expressions = [ExpressionFactory.build_and_get_expression(json_expression) for json_expression in json_data['expressions']]
        return ListExpression(threshold=threshold, threshold_type=threshold_type, expressions=expressions)

    def evaluate_expression(self, sequence, result_container=None):
        
        if result_container == None:
            result_container = ExpressionResultContainer()


class RegistrationRestrictionExpression(Expression):
    expression = models.ArrayField(
        model_container = Expression
    )

    @staticmethod
    def build_and_get_expression(json_data):
        expression = ExpressionFactory.build_and_get_expression(json_data)
        return RegistrationRestrictionExpression(expression=expression)

    def evaluate_expression(self, sequence, result_container=None):
        
        if result_container == None:
            result_container = ExpressionResultContainer()


class YearStandingExpression(Expression):
    threshold_value = models.IntegerField()
    threshold_type = models.CharField(
        max_length = 3,
        choices = [
            ('LT', 'lt'),
            ('LEQ', 'leq'),
            ('EQ', 'eq'),
            ('GEQ', 'geq'),
            ('GT', 'gt')
        ]
    )

    @staticmethod
    def build_and_get_expression(json_data):
        threshold_value = json_data['threshold_value']
        threshold_type = json_data['threshold_type']
        return YearStandingExpression(threshold_value=threshold_value, threshold_type=threshold_type)

    def evaluate_expression(self, sequence, result_container=None):
        
        if result_container == None:
            result_container = ExpressionResultContainer()


class UnitsExpression(Expression):
    threshold_value = models.IntegerField()
    threshold_type = models.CharField(
        max_length = 3,
        choices = [
            ('LT', 'lt'),
            ('LEQ', 'leq'),
            ('EQ', 'eq'),
            ('GEQ', 'geq'),
            ('GT', 'gt')
        ]
    )
    expressions = models.ArrayField(
        model_container = Expression
    )

    @staticmethod
    def build_and_get_expression(json_data):
        threshold_value = json_data['threshold_value']
        threshold_type = json_data['threshold_type']
        expressions = [ExpressionFactory.build_and_get_expression(json_expression) for json_expression in json_data['expressions']]
        return UnitsExpression(threshold_value=threshold_value, threshold_type=threshold_type, expressions=expressions)

    def evaluate_expression(self, sequence, result_container=None):
        if result_container == None:
            result_container = ExpressionResultContainer()


class ExpressionFactory():
    """
    A factory with the mechanism necessary to create expression objects of whatever type is required. The class
    returned from this class may be any child of the `Expression` class
    """

    EXPRESSION_TYPE_MAP = {
        "COURSE": CourseExpression,
        "CONDITIONAL": ConditionalExpression,
        "LIST": ListExpression,
        "REGISTRATION_RESTRICTION": RegistrationRestrictionExpression,
        "YEAR_STANDING": YearStandingExpression,
        "UNITS": UnitsExpression
    }

    @staticmethod
    def build_and_get_expression(json_data):
        expression_model = ExpressionFactory.EXPRESSION_TYPE_MAP[json_data['expression_type']]
        return expression_model.build_and_get_expression(json_data)