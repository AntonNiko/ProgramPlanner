from data import Data
from enum import Enum
import json
import jsonschema
import schema
from utils import ConditionType, RequisiteType, ThresholdType


"""
This is a collection of classes that help build requirements and evaluated if requirements are satisfied. The 
nature of this module is that most classes within this will be used to build an expression. 

It is important to define the semantics of this module:
Expression: A class that represents one statement that must be fulfilled in order for the expression to be 
            fulfilled. An expression, depending on the expression class, might have other nested expressions
            that must be fulfilled before being satisfied itself.
Requirement: A requirement is a list of expressions. This definition is used as a course may contain a list of 
             requirements, each of which must be satisfied.


Note: Although the classes in this module encapsulate the majority of the types of expressions that is provided 
      at UVic, there are some expressions that have not been fully implemented yet. These include:

      - Courses that can only be taken once
      - Courses such as SENG 480B with different topics, where it can be re-taken for credit.
"""
# TODO: Should implement an `ExpressionResult` object that contains information about the evaluated expression.
#       This allows us to include which specific expressions have not been satisfied, as well as attach messages
#       that help diagnose the expression.


class ExpressionType(Enum):
    """
    Identifier for the type of the expression that is being considered. Each expression shall be of one of 
    these types, and have an attribute that references the type
    """

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


class ReferenceExpression():
    """
    This expression represents a pointer to another expressions. The location of the expression 
    is identified by a "group" and "identifier" attribute. These attributes are intended to be 
    implementation agnostic.
    """
    SCHEMA = schema.REFERENCE_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        """
        Returns an instance of this class. Does not return a de-referenced value to which the 
        expression points to.

        Args:
            jsonExpression: A parsed JSON expression to be validated for this class
        """

        jsonschema.validate(jsonExpression, ReferenceExpression.SCHEMA)

        self.expressionType = ExpressionType.REFERENCE
        self.group = jsonExpression["group"]
        self.identifier = jsonExpression["identifier"] 

    def getJsonExpression(self):
        """
        With the initialized ReferenceExpression instance, dereference it and return its JSON expression

        Returns:
            data: The parsed JSON expression from the "group" and "identifier" attributes
        """
        return Data.getData(self.group, self.identifier)

    @staticmethod 
    def buildAndGetExpression(jsonExpression):
        """
        With the provided JSON expression, rA parsed JSON expression to be validated for this classs the 
        de-referenced, built expression

        Args:
            jsonExpression: A parsed JSON expression to be validated and used to build an expression
        Returns:
            expression: A built expression 
        """

        jsonschema.validate(jsonExpression, ReferenceExpression.SCHEMA)

        expression = ReferenceExpression(jsonExpression)
        return Expression.buildAndGetExpression(expression.getJsonExpression())


class CourseExpression():
    """
    This expression refers to a specific course, and its attributes, notably the prerequisite type.
    """

    SCHEMA = schema.COURSE_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        """
        Returns an instance of this class that can be used to check if the expression is satisfied. 

        Args:
            jsonExpression: A parsed JSON expression to be validated and used to build the expression 
        """
        jsonschema.validate(jsonExpression, self.SCHEMA)

        self.expressionType = ExpressionType.COURSE
        self.courseCode = jsonExpression["code"]

        if "requisiteType" not in jsonExpression:
            self.requisiteType = RequisiteType.COREQUISITE
        else:
            self.requisiteType = RequisiteType(jsonExpression["requisiteType"])

    def isExpressionSatisfied(self, activeTerms):
        """
        Determines if the expression, given the `activeTerms` variables, is satisfied
        """

        latestYear = max(activeTerms)
        latestActiveTerm = activeTerms[latestYear][max(activeTerms[latestYear])]

        for year in activeTerms:
            for term in activeTerms[year]:
                if self.courseCode in activeTerms[year][term].getActiveCoursesCodes():
                    # If the course is in the latest active term but we're evaluating as co-requisite, then
                    # not satisfied
                    if (activeTerms[year][term] == latestActiveTerm) and (self.requisiteType == RequisiteType.PREREQUISITE):
                        return False
                    return True
        return False

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

    def isExpressionSatisfied(self, activeTerms):
        if self.condition == ConditionType.OR:
            if self.expressionOne.isExpressionSatisfied(activeTerms) \
               or self.expressionTwo.isExpressionSatisfied(activeTerms):
                return True
            else:
                return False
        elif self.condition == ConditionType.AND:
            if self.expressionOne.isExpressionSatisfied(activeTerms) \
               and self.expressionTwo.isExpressionSatisfied(activeTerms):
               return True
            else:
                return False

        # TODO: Handle undefined state 

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
        if type(jsonExpression["expressions"]) != list:
            reference = ReferenceExpression(jsonExpression["expressions"])
            expressions = reference.getJsonExpression()
        else:
            expressions = jsonExpression["expressions"]

        # Assert threshold is within range 0 to the length of list
        assert self.threshold >= 0 and self.threshold <= len(expressions)

        # At this point, `expressions` is assumed to be a list
        self.expressions = [Expression.buildAndGetExpression(expression) for expression in expressions]

    def isExpressionSatisfied(self, activeTerms):
        expressionsSatisfied = len([expression.isExpressionSatisfied(activeTerms) for expression in self.expressions])

        if self.threshold == ThresholdType.LESS_THAN:
            return expressionsSatisfied < self.threshold
        elif self.threshold == ThresholdType.LESS_THAN_OR_EQUAL:
            return expressionsSatisfied <= self.threshold
        elif self.threshold == ThresholdType.EQUAL:
            return expressionsSatisfied == self.threshold
        elif self.threshold == ThresholdType.GREATER_THAN_OR_EQUAL:
            return expressionsSatisfied >= self.threshold
        elif self.threshold == ThresholdType.GREATER_THAN:
            return expressionsSatisfied > self.threshold

        # TODO: Handle undefined state

    @staticmethod 
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, ListExpression.SCHEMA)
        return ListExpression(jsonExpression)


"""
This is basically a NOT operator on the result of any nested expression. If the nested expression is satisfied,
then the result is not satisfied. If the nested expression is not satisfied, the result is satisfied.
"""
class RegistrationRestrictionExpression():  
    SCHEMA = schema.REGISTRATION_RESTRICTION_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, RegistrationRestrictionExpression.SCHEMA)

        self.expressionType = ExpressionType.REGISTRATION_RESTRICTION
        self.expression = Expression.buildAndGetExpression(jsonExpression["expression"])

    def isExpressionSatisfied(self, activeTerms):
        return not self.expression.isExpressionSatisfied(activeTerms)

    @staticmethod
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, RegistrationRestrictionExpression.SCHEMA)
        return RegistrationRestrictionExpression(jsonExpression)

"""
This is used to determine if in the context of the `activeTerms` that is provided, whether or not the associated
student is part of a range of a year standing.

Since we don't want to keep the definition of the condition to be in this class, we use a reference that define 
your year standing.
"""
class YearStandingExpression():
    SCHEMA = schema.YEAR_STANDING_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, YearStandingExpression.SCHEMA)

        self.expressionType = ExpressionType.YEAR_STANDING
        self.type = jsonExpression["type"]
        self.threshold = ThresholdType(jsonExpression["threshold"])

    """
    Must calculate the number of units completed with help of `UnitsExpression`
    """
    def isExpressionSatisfied(self, activeTerms):
        pass

    @staticmethod
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, YearStandingExpression.SCHEMA)
        return YearStandingExpression(jsonExpression)

"""
Determines whether in the context of `activeTerms`, if the nested expression is satisfied in terms of 
units completed.
"""
class UnitsExpression():
    SCHEMA = schema.UNITS_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, UnitsExpression.SCHEMA)

        self.expressionType = ExpressionType.UNITS
        self.type = jsonExpression["type"]
        self.threshold = ThresholdType(jsonExpression["threshold"])

        # Assert threshold is within range 0 to the length of list
        assert self.threshold >= 0 and self.threshold <= len(jsonExpression["expressions"])

        # At this point, `expressions` is assumed to be a list
        self.expressions = [Expression.buildAndGetExpression(expression) for expression in jsonExpression["expressions"]]
    
    """
    Must calculate the number of units completed in a possibly unbounded number of nested expressions.
    """
    def isExpressionSatisfied(self, activeTerms):
        # TODO: Implement the `ExpressionResults` class to implement this. Otherwise, the alternative
        # is to implement an `unitsSatisfied` for each expression. 
        pass 
    
    @staticmethod 
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, UnitsExpression.SCHEMA)
        return UnitsExpression(jsonExpression)


"""
How do we specify this? Whoever is determining the requirement needs to know the specific courses

Maybe generating a reference is best.

NOTE: Maybe unnecessary and just build an expression by calling Data.getAcademicWritingRequirements()?
"""
class AwrSatisfiedExpression():
    SCHEMA = schema.AWR_SATISFIED_EXPRESSION_SCHEMA

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, AwrSatisfiedExpression.SCHEMA)

        self.expression = Expression.buildAndGetExpression(Data.getAcademicWritingRequirements())

    """
    Evaluates the ACADEMIC_WRITING_REQUIREMENT expression and returns its result
    """ 
    def isExpressionSatisfied(self, activeTerms):
        awrExpression = ReferenceExpression.buildAndGetExpression({
            "group": "uvic_references",
            "identifier": "ACADEMIC_WRITING_REQUIREMENT"
        })

        return awrExpression.isExpressionSatisfied(activeTerms)

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

    """
    Easy to calculate, just count towards the specified level and subject!
    """ 
    def isExpressionSatisfied(self, activeTerms):
        pass

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

    def __init__(self, jsonExpression):
        jsonschema.validate(jsonExpression, RecommendationWarningExpression.SCHEMA)

        self.expressionType = ExpressionType.RECOMMENDATION_WARNING
        self.expression = Expression.buildAndGetExpression(jsonExpression["expression"])

    @staticmethod
    def buildAndGetExpression(jsonExpression):
        jsonschema.validate(jsonExpression, RecommendationWarningExpression.SCHEMA)

        return RecommendationWarningExpression(jsonExpression)


class Expression():
    """
    This is the top-level class of an expression. The root of every expression is an `Expression`
    object. The primary use of the class is for any user to call the `buildAndGetExpression()` 
    function to build a full expression.
    """

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

    def __init__(self, jsonExpression, message=None):
        """
        Returns an `Expression` object with a fully built expression

        Args:
            jsonExpression: A parsed JSON expression to be validated for this class
            message (str): A message to be associated with this expression
        """

        jsonschema.validate(jsonExpression, Expression.SCHEMA)

        expressionClass = Expression.EXPRESSION_TYPE_MAP[jsonExpression["expressionType"]]
        self.expression = expressionClass.buildAndGetExpression(jsonExpression)
        self.message = message

    def isExpressionSatisfied(self, activeTerms):
        return self.expression.isExpressionSatisfied(activeTerms)

    @staticmethod
    def buildAndGetExpression(jsonExpression, message=None):
        jsonschema.validate(jsonExpression, Expression.SCHEMA) 
        return Expression(jsonExpression, message)


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