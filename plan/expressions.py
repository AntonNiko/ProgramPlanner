from enum import Enum
import jsonschema
from .schemas import *


class ConditionType(Enum):
    AND = "AND"
    OR = "OR"


class RequisiteType(Enum):
    PREREQUISITE = "P"
    COREQUISITE = "C"


class ThresholdType(Enum):
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "leq"
    EQUAL = "eq"
    GREATER_THAN_OR_EQUAL = "geq"
    GREATER_THAN = "gt"


class ExpressionResultContainer:

    def __init__(self):
        self.satisfied = False
        self.expression_status = []

    def add_expression_status(self, message, satisfied):
        # The satisfied flag at this level represents the current expression and all its children.
        self.satisfied = satisfied

        if message is None:
            return

        self.expression_status.append({
            'message': message,
            'satisfied': satisfied
        })


class ExpressionType(Enum):
    """
    Identifier for the type of the expression that is being considered. Each expression shall be of one of 
    these types, and have an attribute that references the type
    """

    REFERENCE = "REFERENCE"
    COURSE = "COURSE"
    CONDITIONAL = "CONDITIONAL"
    LIST = "LIST"
    REGISTRATION_RESTRICTION = "REGISTRATION_RESTRICTION"
    YEAR_STANDING = "YEAR_STANDING"
    UNITS = "UNITS"
    AWR_SATISFIED = "AWR_SATISFIED"
    UMBRELLA = "UMBRELLA"
    NO_CREDIT_WARNING = "NO_CREDIT_WARNING"
    RECOMMENDATION_WARNING = "RECOMMENDATION_WARNING"


class Expression:
    """
    This is the parent class of all possible expression types. Ensures by validating the JSON 
    data that the subclass is indeed a valid expression.
    """
    SCHEMA = EXPRESSION_SCHEMA

    def __init__(self, json_data):
        jsonschema.validate(json_data, Expression.SCHEMA)

        self.expression_type = ExpressionType(json_data['expression_type'])

        if 'message' not in json_data:
            self.message = None
        else:
            self.message = json_data['message']


class CourseExpression(Expression):
    """
    This expression refers to a specific course and its attributes, notably the prerequisite associated with it.
    """
    SCHEMA = COURSE_EXPRESSION_SCHEMA

    def __init__(self, json_data):
        """
        Returns an instance of this class that can be used to check if the expression is satisfied. 

        Args:
            json_data: A parsed JSON expression to be validated and used to build the expression 
        """

        jsonschema.validate(json_data, self.SCHEMA)

        super().__init__(json_data)

        self.subject = json_data['subject']
        self.number = json_data['number']

        if "requisite_type" not in json_data:
            self.requisite_type = RequisiteType.COREQUISITE
        else:
            self.requisite_type = RequisiteType(json_data["requisite_type"])

    @staticmethod
    def build_and_get_expression(json_data):
        jsonschema.validate(json_data, CourseExpression.SCHEMA)
        return CourseExpression(json_data)

    def evaluate_expression(self, sequence, result_container=None):
        """
        Determines if the expression, given the sequence, is satisfied

        Args:
            activeTerms: A dictionary containing the list of courses to evaluate
        Returns:
            (boolean): True if the expression is satisfied, false otherwise
        """
        if result_container is None:
            result_container = ExpressionResultContainer()

        latest_term = max(sequence.terms)
        sorted_terms = sequence.terms.copy()
        sorted_terms.sort()

        for term in sorted_terms:
            for course in term.courses:
                if (course.course_code.subject == self.subject) and (course.course_code.number == self.number):
                    if (self.requisite_type == RequisiteType.PREREQUISITE) and (
                            term.year == latest_term.year and term.term_type == latest_term.term_type):
                        result_container.add_expression_status(self.message, False)
                        return result_container

                    result_container.add_expression_status(self.message, True)
                    return result_container

        result_container.add_expression_status(self.message, False)
        return result_container


class ConditionalExpression(Expression):
    SCHEMA = CONDITIONAL_EXPRESSION_SCHEMA

    def __init__(self, json_data):
        jsonschema.validate(json_data, ConditionalExpression.SCHEMA)

        super().__init__(json_data)

        self.expression_one = ExpressionFactory.build_and_get_expression(json_data['expression_one'])
        self.expression_two = ExpressionFactory.build_and_get_expression(json_data['expression_two'])
        self.condition = ConditionType(json_data['condition'])

    @staticmethod
    def build_and_get_expression(json_data):
        jsonschema.validate(json_data, ConditionalExpression.SCHEMA)
        return ConditionalExpression(json_data)

    def evaluate_expression(self, sequence, result_container=None):
        if result_container is None:
            result_container = ExpressionResultContainer()

        if self.condition == ConditionType.OR:
            if self.expression_one.evaluate_expression(sequence, result_container).satisfied \
                    or self.expression_two.evaluate_expression(sequence, result_container).satisfied:
                result_container.add_expression_status(self.message, True)
            else:
                result_container.add_expression_status(self.message, False)

        elif self.condition == ConditionType.AND:
            if self.expression_one.evaluate_expression(sequence, result_container).satisfied \
                    and self.expression_two.evaluate_expression(sequence, result_container).satisfied:
                result_container.add_expression_status(self.message, True)
            else:
                result_container.add_expression_status(self.message, False)

        else:
            # TODO: Raise an exception since this expression CANNOT be evaluated. This is an error.
            pass

        return result_container


class ListExpression(Expression):
    SCHEMA = LIST_EXPRESSION_SCHEMA

    def __init__(self, json_data):
        jsonschema.validate(json_data, ListExpression.SCHEMA)

        super().__init__(json_data)

        self.threshold_value = json_data['threshold_value']
        self.threshold_type = ThresholdType(json_data['threshold_type'])
        self.expressions = [ExpressionFactory.build_and_get_expression(expression) for expression in
                            json_data['expressions']]

    @staticmethod
    def build_and_get_expression(json_data):
        jsonschema.validate(json_data, ListExpression.SCHEMA)
        return ListExpression(json_data)

    def evaluate_expression(self, sequence, result_container=None):
        if result_container is None:
            result_container = ExpressionResultContainer()

        satisfied_expressions = len([True for expression in self.expressions if
                                     expression.evaluate_expressions(sequence, result_container).satisfied])

        if self.threshold_type == ThresholdType.LESS_THAN:
            result_container.add_expression_status(self.message, satisfied_expressions < self.threshold_value)
        elif self.threshold_type == ThresholdType.LESS_THAN_OR_EQUAL:
            result_container.add_expression_status(self.message, satisfied_expressions <= self.threshold_value)
        elif self.threshold_type == ThresholdType.EQUAL:
            result_container.add_expression_status(self.message, satisfied_expressions == self.threshold_value)
        elif self.threshold_type == ThresholdType.GREATER_THAN_OR_EQUAL:
            result_container.add_expression_status(self.message, satisfied_expressions >= self.threshold_value)
        elif self.threshold_type == ThresholdType.GREATER_THAN:
            result_container.add_expression_status(self.message, satisfied_expressions > self.threshold_value)
        else:
            # TODO: Raise an exception since this expression CANNOT be evaluated. This is an error.
            pass

        return result_container


class RegistrationRestrictionExpression(Expression):
    SCHEMA = REGISTRATION_RESTRICTION_EXPRESSION_SCHEMA

    def __init__(self, json_data):
        jsonschema.validate(json_data, RegistrationRestrictionExpression.SCHEMA)

        super().__init__(json_data)

        self.expression = ExpressionFactory.build_and_get_expression(json_data['expression'])

    @staticmethod
    def build_and_get_expression(json_data):
        jsonschema.validate(json_data, RegistrationRestrictionExpression.SCHEMA)
        return RegistrationRestrictionExpression(json_data)

    def evaluate_expression(self, sequence, result_container=None):
        if result_container is None:
            result_container = ExpressionResultContainer()

        result_container.add_expression_status(self.message,
                                               not self.expression.evaluate_expression(sequence, result_container))
        return result_container


class ExpressionFactory():
    """
    A factory with the mechanism necessary to create expression objects of whatever type is required. The class
    returned from this class may be any child of the `Expression` class
    """

    EXPRESSION_TYPE_MAP = {
        "COURSE": CourseExpression,
        "CONDITIONAL": ConditionalExpression,
        "LIST": ListExpression,
        "REGISTRATION_RESTRICTION": RegistrationRestrictionExpression
    }

    @staticmethod
    def build_and_get_expression(json_data):
        expression_class = ExpressionFactory.EXPRESSION_TYPE_MAP[json_data['expression_type']]
        return expression_class.build_and_get_expression(json_data)
