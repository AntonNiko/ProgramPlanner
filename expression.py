#from course import CourseCode
from data import Data
from enum import Enum
import json
import jsonschema
import schema
from utils import ConditionType, RequisiteType, ThresholdType


# THE REQUIREMENTS MUST BE A LIST OF EXPRESSIONS. Each element of the list is a requirement statement
# Possible list of requirements expression that must be implemented

# Other exceptional expressions to implement:
#
# - COURSE can only be taken once
# - Courses such as SENG480B when different topics  

class ExpressionType(Enum):
    REFERENCE = 1
    COURSE = 2
    CONDITIONAL = 3
    LIST = 4
    REGISTRATION_RESTRICTION = 5
    YEAR_STANDING = 6
    UNITS = 7
    AWR_SATISFIED = 8
    UMBRELLA = 9
    NO_CREDIT_WARNING = 10
    RECOMMENDATION_WARNING = 11

"""
This is effectively a pointer to another expression. The location of the expression is specified.

__init__: Fetches simply the expression without de-referencing the object
buildAndGetExpression: Meant to return an instance of ReferenceExpression without de-referencing
"""
class ReferenceExpression():
    SCHEMA = schema.REFERENCE_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, ReferenceExpression.SCHEMA)

        self.expressionType = ExpressionType.REFERENCE
        self.group = jsonExpression["group"]
        self.identifier = jsonExpression["identifier"] 

    """
    With the initialized ReferenceExpression instance, dereference and get its json expression
    """
    def getJsonExpression(self):
        return Data.getData(self.group, self.identifier)

    @staticmethod 
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, ReferenceExpression.SCHEMA)

        expression = ReferenceExpression(jsonExpression)
        return Expression.buildAndGetExpression(expression.getJsonExpression())


class CourseExpression():
    SCHEMA = schema.COURSE_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, self.SCHEMA)

        self.expressionType = ExpressionType.COURSE
        self.courseCode = jsonExpression["code"]

        if "requisiteType" not in jsonExpression:
            self.requisiteType = RequisiteType.PREREQUISITE
        else:
            self.requisiteType = RequisiteType(jsonExpression["requisiteType"])

    @staticmethod 
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, CourseExpression.SCHEMA)
        return CourseExpression(jsonExpression) 


class ConditionalExpression():
    SCHEMA = schema.CONDITIONAL_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, ConditionalExpression.SCHEMA)

        self.expressionType = ExpressionType.CONDITIONAL
        self.expressionOne  = Expression.buildAndGetExpression(jsonExpression["expressionOne"])
        self.expressionTwo  = Expression.buildAndGetExpression(jsonExpression["expressionTwo"])
        self.condition      = ConditionType(jsonExpression["condition"])

    @staticmethod
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, ConditionalExpression.SCHEMA)
        return ConditionalExpression(jsonExpression)


"""

Aside: Having simply a list of expressions, without context, has no purpose. What exactly is the point
of it? The context that I see is only that a list complements a List Expression, no 
other expression.

The list storage will be directly coupled to the List expression.

- jsonExpression["expressions"] *can* be a reference to a list, or just a list

"""
class ListExpression():
    SCHEMA = schema.LIST_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, ListExpression.SCHEMA)

        self.expressionType = ExpressionType.LIST 
        self.threshold = jsonExpression["threshold"]
        self.type = ThresholdType(jsonExpression["type"])

        # If the type of "expressions" is not reference we de-reference
        if type(jsonExpression["expression"]) != list:
            reference = ReferenceExpression(jsonExpression["expression"])
            expressions = reference.getJsonExpression()
        else:
            expressions = jsonExpression["expressions"]

        # At this point, `expressions` is assumed to be a list
        self.expressions = [Expression.buildAndGetExpression(expression) for expression in expressions]

    @staticmethod 
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, ListExpression.SCHEMA)
        return ListExpression(jsonExpression)


# TODO: Restrict to one expression, or a list of expressions? 
class RegistrationRestrictionExpression():  
    SCHEMA = schema.REGISTRATION_RESTRICTION_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, RegistrationRestrictionExpression.SCHEMA)

        self.expressionType = ExpressionType.REGISTRATION_RESTRICTION
        self.expression = Expression.buildAndGetExpression(jsonExpression["expression"])

    @staticmethod
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, RegistrationRestrictionExpression.SCHEMA)
        return RegistrationRestrictionExpression(jsonExpression)


class YearStandingExpression():
    SCHEMA = schema.YEAR_STANDING_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, YearStandingExpression.SCHEMA)

        self.expressionType = ExpressionType.YEAR_STANDING
        self.type = jsonExpression["type"]
        self.threshold = ThresholdType(jsonExpression["threshold"])

    @staticmethod
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, YearStandingExpression.SCHEMA)
        return YearStandingExpression(jsonExpression)


class UnitsExpression():
    SCHEMA = schema.UNITS_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, UnitsExpression.SCHEMA)

        self.expressionType = ExpressionType.UNITS
        self.type = jsonExpression["type"]
        self.threshold = ThresholdType(jsonExpression["threshold"])

    @staticmethod 
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, UnitsExpression.SCHEMA)
        return UnitsExpression(jsonExpression)


"""
How do we specify this? Whoever is determining the requirement needs to know the specific courses

Maybe generating a reference is best.
"""
class AwrSatisfiedExpression():
    SCHEMA = schema.AWR_SATISFIED_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, AwrSatisfiedExpression.SCHEMA)

        self.expression = Expression.buildAndGetExpression(Data.getAcademicWritingRequirements())

    @staticmethod
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, AwrSatisfiedExpression.SCHEMA)
        return AwrSatisfiedExpression(jsonExpression)

class UmbrellaExpression():
    SCHEMA = schema.UMBRELLA_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, UmbrellaExpression.SCHEMA) 

        self.level = jsonExpression["level"]
        self.subject = jsonExpression["subject"]

    @staticmethod
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, UmbrellaExpression.SCHEMA)
        return UmbrellaExpression(jsonExpression)


class NoCreditWarningExpression():
    SCHEMA = schema.NO_CREDIT_WARNING_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, NoCreditWarningExpression.SCHEMA)

        self.expressionType = ExpressionType.NO_CREDIT_WARNING
        self.expression = Expression.buildAndGetExpression(jsonExpression["expression"])

    @staticmethod
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, NoCreditWarningExpression.SCHEMA)
        return NoCreditWarningExpression(jsonExpression)


class RecommendationWarningExpression():
    SCHEMA = schema.RECOMMENDATION_WARNING_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression, message):
        jsonschema.validate(jsonExpression, RecommendationWarningExpression.SCHEMA)
        assert type(message) == str 

        self.expressionType = ExpressionType.RECOMMENDATION_WARNING
        self.expression = Expression.buildAndGetExpression(jsonExpression["expression"])
        self.message = message

    @staticmethod
    def buildAndGetExpression(jsonExpression, message):
        jsonschema.validate(jsonExpression, RecommendationWarningExpression.SCHEMA)
        assert type(message) == str

        return RecommendationWarningExpression(jsonExpression, message)


class Expression():
    SCHEMA = schema.EXPRESSION_SCHEMA
    EXPRESSION_TYPE_MAP = {
        "REFERENCE": ReferenceExpression,
        "COURSE": CourseExpression,
        "CONDITIONAL": ConditionalExpression,
        "LIST": ListExpression,
        "REGISTRATION_RESTRICTION": RegistrationRestrictionExpression,
        "YEAR_STANDING": YearStandingExpression,
        "UNITS": UnitsExpression,
        "AWR_STANDING": AwrSatisfiedExpression,
        "UMBRELLA": UmbrellaExpression,
        "NO_CREDIT_WARNING": NoCreditWarningExpression,
        "RECOMMENDATION_WARNING": RecommendationWarningExpression
    }

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, Expression.SCHEMA)

        expressionClass = Expression.EXPRESSION_TYPE_MAP[jsonExpression["expressionType"]]
        self.expression = expressionClass.buildAndGetExpression(jsonExpression)

    @staticmethod
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, Expression.SCHEMA) 
        return Expression(jsonExpression)


if __name__ == "__main__":
    testExpression = {
        "expressionType": "CONDITIONAL",
        "expressionOne": {
            "expressionType": "COURSE",
            "code": "CSC 110",
            "requisiteType": "P"
        },
        "expressionTwo": {
            "expressionType": "COURSE",
            "code": "CSC 111",
            "requisiteType": "C"
        },
        "condition": "OR"
    }

    e = Expression.buildAndGetExpression(testExpression)




"""
    testRequirements = [
        {
            "expressionType": "CONDITIONAL",
            "expressionOne": {
                "expressionType": "COURSE",
                "code": "CSC 110",
                "requisiteType": "P"
            },
            "expressionTwo": {
                "expressionType": "COURSE",
                "code": "CSC 111",
                "requisiteType": "C"
            },
            "condition": "OR" # Can be OR or AND
        },
        {
            "expressionType": "LIST",
            "threshold": 1,
            "type": "geq", # Can be lt, leq, eq, geq, gt (less than, less than eq, equal, greater than eq, greater than)
            "expressions": [{
                "code": "ENGR 110",
                "requisiteType": "P"
            },
            {
                "code": "ENGR 111",
                "requisiteType": "P"
            },
            {
                "code": "ENGR 112",
                "requisiteType": "P"
            }]
        },
        {
            "expressionType": "COURSE",
            "code": "ENGR 112",
            "requisiteType": "P"
        },
        #{
        #    "expressionType": "CREDIT_RESTRICTION", # Cannot take if already have credit 
        #    "expression": {
                # Any expression type, ignores prerequisite/corequisites
        #    }
        #},
        {
            "expressionType": "NO_CREDIT_WARNING", # Cannot get credit if already have credit
            "expression": {
                # Any expression type, ignores prerequisites/corequisites
            }
        },
        {
            "expressionType": "RECCOMENDATION_WARNING",
            "expression": {
                
            }
        },
        {
            "expressionType": "REGISTRSATION_RESTRICTION", # Basically NOT. To allow for "cannot take if also registered in...".  CREDIT_RESTRICTION can be fulfilled by this
            "expression": {
                # Any expression type, ignores prerequisite/corequisites
            }
        },
        {
            "expressionType": "YEAR_STANDING",
            "type": "leq", # Can be lt, leq, eq, geq, gt (less than, less than eq, equal, greater than eq, greater than)
            "threshold": 4 # 1) First year 2) Second year 3) Third year 4) Fourth year
        },
        {
            "expressionType": "AWR_SATISFIED"
        }
    ]
"""