#from course import CourseCode
from enum import Enum
import jsonschema
import schema

# THE REQUIREMENTS MUST BE A LIST OF EXPRESSIONS. Each element of the list is a requirement statement
# Possible list of requirements expression that must be implemented

# Other exceptional expressions:
#
# - COURSE can only be taken once
# - Courses such as SENG480B when different topics  
# - "3.0 units in 200 or 300-level MATH or STAT courses"
#
# Include recommendations? I think so since this is the best place for that, to tie it to requirements in case,
# and to inform user

class ExpressionType(Enum):
    COURSE = 1
    CONDITIONAL = 2
    LIST = 3
    CREDIT_RESTRICTION = 4
    REGISTRATION_RESTRICTION = 5
    NO_CREDIT_WARNING = 6
    RECOMMENDATION_WARNING = 7
    YEAR_STANDING = 8
    AWR_SATISFIED = 9

""" 
Represents the requirement that must be satisfied to take a course. An instance of this 
class shall be composed into an instance of a Course class.  

The requirement is a list of expressions. Each top-level expresison must be satisfied for 
the requirmeent to be satisfied.

Do we pass in the entire sequence in here to find out if it is satisfied? Probably better 
in the sequence object. It already has all the info it needs. Can call a requirement 
intepreter/manager or something

"""
class Requirement():
    def __init__(self, jsonRequirements):
        assert type(jsonRequirements) == list 

        self.expressions = [Expression.buildAndGetExpression(expressionJson) for expressionJson in jsonRequirements]


class CourseExpression():
    SCHEMA = schema.COURSE_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, self.SCHEMA)

        self.expressionType = ExpressionType.COURSE
        self.courseCode = jsonExpression["code"]
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


class ListExpression():
    SCHEMA = schema.LIST_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, ListExpression.SCHEMA)

        self.expressionType = ExpressionType.LIST 
        self.threshold = jsonExpression["threshold"]
        self.type = jsonExpression["type"]
        self.expressions = [Expression.buildAndGetExpression(expression) for expression in jsonExpression["expressions"]]

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
        self.threshold = jsonExpression["threshold"]

    @staticmethod
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, YearStandingExpression.SCHEMA)
        return YearStandingExpression(jsonExpression)


class AwrSatisfiedExpression():

    def __init__(self, jsonExpression):
        pass

    @staticmethod
    def buildAndGetExpression(jsonExpression):
        pass


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

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, RecommendationWarningExpression.SCHEMA)

        self.expressionType = ExpressionType.RECOMMENDATION_WARNING
        self.expression = Expression.buildAndGetExpression(jsonExpression["expression"])

    @staticmethod
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, RecommendationWarningExpression.SCHEMA)
        return RecommendationWarningExpression(jsonExpression)


class Expression():
    SCHEMA = schema.EXPRESSION_SCHEMA
    EXPRESSION_TYPE_MAP = {
        "COURSE": CourseExpression,
        "CONDITIONAL": ConditionalExpression,
        "LIST": ListExpression,
        "REGISTRATION_RESTRICTION": RegistrationRestrictionExpression,
        "YEAR_STANDING": YearStandingExpression,
        "AWR_STANDING": AwrSatisfiedExpression,
        "NO_CREDIT_WARNING": NoCreditWarningExpression,
        "RECOMMENDATION_WARNING": RecommendationWarningExpression
    }

    @staticmethod
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, Expression.SCHEMA) 

        expressionClass = Expression.EXPRESSION_TYPE_MAP[jsonExpression["expressionType"]]
        return expressionClass(jsonExpression)


class RequisiteType(Enum):
    PREREQUISITE = "P"
    COREQUISITE  = "C"

class ConditionType(Enum):
    AND = "AND"
    OR = "OR"

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
        "condition": "OR" # Can be OR or AND
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