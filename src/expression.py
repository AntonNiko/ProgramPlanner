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


class ResultContainer():
    """
    This class is intended to be injected into an `Expression` method to contain information on 
    the result of the evaluation. Furthermore, certain attributes are used to calculate statistics,
    such as units completed.
    """
    
    def __init__(self):
        # Indicates that the expression in which this value is being evaluated at is satisfied
        self.satisfied = False

        # A list of dictionary elements composed of messages relating to an expression, and its satisfied status
        self.expressionStatus = []
        self.satisfiedUnits = 0

    def addExpressionStatus(self, message, isSatisfied):
        """
        Adds the result of an expression being evaluated. Furthermore, updates the status the `satisfied`
        variable to reflect the status of the expression. Used to diagnose which specific expressions with 
        messages have or have not been satisfied.
        """

        self.satisfied = isSatisfied

        if message == None:
            return

        self.expressionStatus.append({
            "message": message,
            "isSatisfied": isSatisfied
        })


class Expression():
    """
    This is the parent class of all possible expression types. Ensures by validating the JSON 
    data that the subclass is indeed a valid expression.
    """

    SCHEMA = schema.EXPRESSION_SCHEMA

    def __init__(self, jsonData):
        jsonschema.validate(jsonData, Expression.SCHEMA)

        self.expressionType = ExpressionType(jsonData["expressionType"])

        if "message" not in jsonData:
            self.message = None
        else:
            self.message = jsonData["message"]


class ReferenceExpression(Expression):
    """
    This expression represents a pointer to another expressions. The location of the expression 
    is identified by a "group" and "identifier" attribute. These attributes are intended to be 
    agnostic of the data storage mechanism.

    This class is unique among other expressions, since in the normal use case, we return the `Expression`
    child that is pointed to by this reference.
    """

    SCHEMA = schema.REFERENCE_EXPRESSION_SCHEMA

    def __init__(self, jsonData):
        """
        Returns an instance of this class. Does not return a de-referenced value to which the 
        expression points to.

        Args:
            jsonData: A parsed JSON expression to be validated for this class
        """

        jsonschema.validate(jsonData, ReferenceExpression.SCHEMA)

        super().__init__(jsonData)

        self.group = jsonData["group"]
        self.identifier = jsonData["identifier"] 

    def getJsonData(self):
        """
        With the initialized ReferenceExpression instance, dereference it and return its JSON expression

        Returns:
            data: The parsed JSON expression from the "group" and "identifier" attributes
        """

        return Data.getData(self.group, self.identifier)

    @staticmethod 
    def buildAndGetExpression(jsonData):
        """
        With the provided JSON expression, rA parsed JSON expression to be validated for this classs the 
        de-referenced, built expression

        Args:
            jsonData: A parsed JSON expression to be validated and used to build an expression
        Returns:
            expression: A built expression from the de-referenced JSON data
        """

        jsonschema.validate(jsonData, ReferenceExpression.SCHEMA)

        expression = ReferenceExpression(jsonData)
        return ExpressionFactory.buildAndGetExpression(expression.getJsonData())


class CourseExpression(Expression):
    """
    This expression refers to a specific course and its attributes, notably the prerequisite associated with it.
    """

    SCHEMA = schema.COURSE_EXPRESSION_SCHEMA

    def __init__(self, jsonData):
        """
        Returns an instance of this class that can be used to check if the expression is satisfied. 

        Args:
            jsonData: A parsed JSON expression to be validated and used to build the expression 
        """

        jsonschema.validate(jsonData, self.SCHEMA)

        super().__init__(jsonData)

        self.courseCode = jsonData["code"]

        if "requisiteType" not in jsonData:
            self.requisiteType = RequisiteType.COREQUISITE
        else:
            self.requisiteType = RequisiteType(jsonData["requisiteType"])

    def isExpressionSatisfied(self, activeTerms, resultContainer=None):
        """
        Determines if the expression, given the `activeTerms` variables, is satisfied

        Args:
            activeTerms: A dictionary containing the list of courses to evaluate
        Returns:
            (boolean): True if the expression is satisfied, false otherwise
        """

        if resultContainer == None:
            resultContainer = ResultContainer()

        latestYear = max(activeTerms)
        latestActiveTerm = activeTerms[latestYear][max(activeTerms[latestYear])]

        for year in activeTerms:
            for term in activeTerms[year]:
                if self.courseCode in activeTerms[year][term].getActiveCoursesCodes():
                    # If the course is in the latest active term but we're evaluating as co-requisite, then
                    # not satisfied
                    if (activeTerms[year][term] == latestActiveTerm) and (self.requisiteType == RequisiteType.PREREQUISITE):
                        #resultContainer.satisfied = False
                        resultContainer.addExpressionStatus(self.message, False)
                        return resultContainer

                    #resultContainer.satisfied = True
                    resultContainer.addExpressionStatus(self.message, True)
                    return resultContainer

        #resultContainer.satisfied = False    
        resultContainer.addExpressionStatus(self.message, False)
        return resultContainer

    @staticmethod 
    def buildAndGetExpression(jsonData):
        jsonschema.validate(jsonData, CourseExpression.SCHEMA)
        return CourseExpression(jsonData) 


class ConditionalExpression(Expression):
    """
    This expression refers to a condition which must be satisfied by the two nested expressions. The condition
    associated with this expression must be a type specified by `ConditionType`
    """

    SCHEMA = schema.CONDITIONAL_EXPRESSION_SCHEMA

    def __init__(self, jsonData):
        jsonschema.validate(jsonData, ConditionalExpression.SCHEMA)

        super().__init__(jsonData)

        self.expressionOne  = ExpressionFactory.buildAndGetExpression(jsonData["expressionOne"])
        self.expressionTwo  = ExpressionFactory.buildAndGetExpression(jsonData["expressionTwo"])
        self.condition      = ConditionType(jsonData["condition"])

    def isExpressionSatisfied(self, activeTerms, resultContainer=None):
        """
        Determines if the expression, given the `activeTerms` variables, is satisfied

        Args:
            activeTerms: A dictionary containing the list of courses to evaluate
        Returns:
            (boolean): True if the expression is satisfied, false otherwise
        """

        if resultContainer == None:
            resultContainer = ResultContainer()

        if self.condition == ConditionType.OR:
            if self.expressionOne.isExpressionSatisfied(activeTerms, resultContainer).satisfied \
               or self.expressionTwo.isExpressionSatisfied(activeTerms, resultContainer).satisfied:
                #resultContainer.satisfied = True
                resultContainer.addExpressionStatus(self.message, True)
            else:
                #resultContainer.satisfied = False
                resultContainer.addExpressionStatus(self.message, False)

        elif self.condition == ConditionType.AND:
            if self.expressionOne.isExpressionSatisfied(activeTerms, resultContainer).satisfied \
               and self.expressionTwo.isExpressionSatisfied(activeTerms, resultContainer).satisfied:
                #resultContainer.satisfied = True
                resultContainer.addExpressionStatus(self.message, True)
            else:
                #resultContainer.satisfied = False
                resultContainer.addExpressionStatus(self.message, False)

        else:
            # TODO: Raise an exception since this expression CANNOT be evaluated. This is an error.
            pass

        return resultContainer

    @staticmethod
    def buildAndGetExpression(jsonData):
        jsonschema.validate(jsonData, ConditionalExpression.SCHEMA)
        return ConditionalExpression(jsonData)


class ListExpression(Expression):
    """
    This expression refers to a list of expressions with an associated condition that must be satisfied 
    for the expression to be satisfied.
    """

    SCHEMA = schema.LIST_EXPRESSION_SCHEMA

    def __init__(self, jsonData):
        jsonschema.validate(jsonData, ListExpression.SCHEMA)

        super().__init__(jsonData)

        self.threshold = jsonData["threshold"]
        self.type = ThresholdType(jsonData["type"])

        # If the type of "expressions" is not reference, de-reference
        if type(jsonData["expressions"]) != list:
            reference = ReferenceExpression(jsonData["expressions"])
            expressions = reference.getJsonData()
        else:
            expressions = jsonData["expressions"]

        # At this point, `expressions` is assumed to be a list
        self.expressions = [ExpressionFactory.buildAndGetExpression(expression) for expression in expressions]

    def isExpressionSatisfied(self, activeTerms, resultContainer=None):
        """
        Determines if the expression, given the `activeTerms` variables, is satisfied

        Args:
            activeTerms: A dictionary containing the list of courses to evaluate
        Returns:
            (boolean): True if the expression is satisfied, false otherwise
        """
        
        if resultContainer == None:
            resultContainer = ResultContainer()

        expressionsSatisfied = len([True for expression in self.expressions if expression.isExpressionSatisfied(activeTerms, resultContainer).satisfied])

        if self.type == ThresholdType.LESS_THAN:
            resultContainer.addExpressionStatus(self.message, expressionsSatisfied < self.threshold)
        elif self.type == ThresholdType.LESS_THAN_OR_EQUAL:
            resultContainer.addExpressionStatus(self.message, expressionsSatisfied <= self.threshold)
        elif self.type == ThresholdType.EQUAL:
            resultContainer.addExpressionStatus(self.message, expressionsSatisfied == self.threshold)
        elif self.type == ThresholdType.GREATER_THAN_OR_EQUAL:
            resultContainer.addExpressionStatus(self.message, expressionsSatisfied >= self.threshold)
        elif self.type == ThresholdType.GREATER_THAN:
            resultContainer.addExpressionStatus(self.message, expressionsSatisfied > self.threshold)
        else:
            # TODO: Raise an exception since this expression CANNOT be evaluated. This is an error.
            pass            

        return resultContainer

    @staticmethod 
    def buildAndGetExpression(jsonData):
        jsonschema.validate(jsonData, ListExpression.SCHEMA)
        return ListExpression(jsonData)


"""
This is basically a NOT operator on the result of any nested expression. If the nested expression is satisfied,
then the result is not satisfied. If the nested expression is not satisfied, the result is satisfied.
"""
class RegistrationRestrictionExpression(Expression):  
    SCHEMA = schema.REGISTRATION_RESTRICTION_EXPRESSION_SCHEMA

    def __init__(self, jsonData):
        jsonschema.validate(jsonData, RegistrationRestrictionExpression.SCHEMA)

        super().__init__(jsonData)

        self.expression = ExpressionFactory.buildAndGetExpression(jsonData["expression"])

    def isExpressionSatisfied(self, activeTerms, resultContainer=None):
        """
        Determines if the expression, given the `activeTerms` variables, is satisfied

        Args:
            activeTerms: A dictionary containing the list of courses to evaluate
        Returns:
            (boolean): True if the expression is satisfied, false otherwise
        """

        if resultContainer == None:
            result = ResultContainer()

        result.addExpressionStatus(self.message, not self.expression.isExpressionSatisfied(activeTerms))
        return result

    @staticmethod
    def buildAndGetExpression(jsonData):
        jsonschema.validate(jsonData, RegistrationRestrictionExpression.SCHEMA)
        return RegistrationRestrictionExpression(jsonData)


"""
This is used to determine if in the context of the `activeTerms` that is provided, whether or not the associated
student is part of a range of a year standing.

Since we don't want to keep the definition of the condition to be in this class, we use a reference that define 
your year standing.
"""
class YearStandingExpression(Expression):
    SCHEMA = schema.YEAR_STANDING_EXPRESSION_SCHEMA

    def __init__(self, jsonData):
        jsonschema.validate(jsonData, YearStandingExpression.SCHEMA)

        super().__init__(jsonData)

        self.type = jsonData["type"]
        self.threshold = ThresholdType(jsonData["threshold"])

    def isExpressionSatisfied(self, activeTerms, resultContainer=None):
        """
        Determines if the expression, given the `activeTerms` variables, is satisfied

        Args:
            activeTerms: A dictionary containing the list of courses to evaluate
        Returns:
            (boolean): True if the expression is satisfied, false otherwise
        """

        if resultContainer == None:
            result = ResultContainer()

    @staticmethod
    def buildAndGetExpression(jsonData):
        jsonschema.validate(jsonData, YearStandingExpression.SCHEMA)
        return YearStandingExpression(jsonData)


"""
Determines whether in the context of `activeTerms`, the nested expression is satisfied in terms of 
units completed.
"""
class UnitsExpression(Expression):
    SCHEMA = schema.UNITS_EXPRESSION_SCHEMA

    def __init__(self, jsonData):
        jsonschema.validate(jsonData, UnitsExpression.SCHEMA)

        super().__init__(jsonData)

        self.type = jsonData["type"]
        self.threshold = ThresholdType(jsonData["threshold"])

        # Assert threshold is within range 0 to the length of list
        assert self.threshold >= 0 and self.threshold <= len(jsonData["expressions"])

        # At this point, `expressions` is assumed to be a list
        self.expressions = [ExpressionFactory.buildAndGetExpression(expression) for expression in jsonData["expressions"]]
    
    def isExpressionSatisfied(self, activeTerms, resultContainer=None):
        """
        Determines if the expression, given the `activeTerms` variables, is satisfied

        Args:
            activeTerms: A dictionary containing the list of courses to evaluate
        Returns:
            (boolean): True if the expression is satisfied, false otherwise
        """

        # TODO: Implement the `ExpressionResults` class to implement this. Otherwise, the alternative
        # is to implement an `unitsSatisfied` for each expression. 

        if resultContainer == None:
            result = ResultContainer()

        
    
    @staticmethod 
    def buildAndGetExpression(jsonData):
        jsonschema.validate(jsonData, UnitsExpression.SCHEMA)
        return UnitsExpression(jsonData)


"""
How do we specify this? Whoever is determining the requirement needs to know the specific courses

Maybe generating a reference is best.

NOTE: Maybe unnecessary and just build an expression by calling Data.getAcademicWritingRequirements()?
"""
class AwrSatisfiedExpression(Expression):
    SCHEMA = schema.AWR_SATISFIED_EXPRESSION_SCHEMA

    def __init__(self, jsonData):
        jsonschema.validate(jsonData, AwrSatisfiedExpression.SCHEMA)

        super().__init__(jsonData)

        self.expression = ExpressionFactory.buildAndGetExpression(Data.getAcademicWritingRequirements())

    """
    Evaluates the ACADEMIC_WRITING_REQUIREMENT expression and returns its result
    """ 
    def isExpressionSatisfied(self, activeTerms, resultContainer=None):
        """
        Determines if the expression, given the `activeTerms` variables, is satisfied

        Args:
            activeTerms: A dictionary containing the list of courses to evaluate
        Returns:
            (boolean): True if the expression is satisfied, false otherwise
        """

        if resultContainer == None:
            result = ResultContainer()

        awrExpression = ReferenceExpression.buildAndGetExpression({
            "group": "uvic_references",
            "identifier": "ACADEMIC_WRITING_REQUIREMENT"
        })

        return awrExpression.isExpressionSatisfied(activeTerms)

    @staticmethod
    def buildAndGetExpression(jsonData):
        jsonschema.validate(jsonData, AwrSatisfiedExpression.SCHEMA)
        return AwrSatisfiedExpression(jsonData)


class UmbrellaExpression(Expression):
    SCHEMA = schema.UMBRELLA_EXPRESSION_SCHEMA

    def __init__(self, jsonData):
        jsonschema.validate(jsonData, UmbrellaExpression.SCHEMA) 

        super().__init__(jsonData)

        self.level = jsonData["level"]
        self.subject = jsonData["subject"]

    """
    Easy to calculate, just count towards the specified level and subject!
    """ 
    def isExpressionSatisfied(self, activeTerms, resultContainer=None):
        """
        Determines if the expression, given the `activeTerms` variables, is satisfied

        Args:
            activeTerms: A dictionary containing the list of courses to evaluate
        Returns:
            (boolean): True if the expression is satisfied, false otherwise
        """

        if resultContainer == None:
            result = ResultContainer()

    @staticmethod
    def buildAndGetExpression(jsonData):
        jsonschema.validate(jsonData, UmbrellaExpression.SCHEMA)
        return UmbrellaExpression(jsonData)


class NoCreditWarningExpression(Expression):
    SCHEMA = schema.NO_CREDIT_WARNING_EXPRESSION_SCHEMA

    def __init__(self, jsonData):
        jsonschema.validate(jsonData, NoCreditWarningExpression.SCHEMA)

        super().__init__(jsonData)

        self.expression = ExpressionFactory.buildAndGetExpression(jsonData["expression"])

    @staticmethod
    def buildAndGetExpression(jsonData):
        jsonschema.validate(jsonData, NoCreditWarningExpression.SCHEMA)
        return NoCreditWarningExpression(jsonData)


class RecommendationWarningExpression(Expression):
    SCHEMA = schema.RECOMMENDATION_WARNING_EXPRESSION_SCHEMA

    def __init__(self, jsonData):
        jsonschema.validate(jsonData, RecommendationWarningExpression.SCHEMA)

        super().__init__(jsonData)

        self.expression = ExpressionFactory.buildAndGetExpression(jsonData["expression"])

    @staticmethod
    def buildAndGetExpression(jsonData):
        jsonschema.validate(jsonData, RecommendationWarningExpression.SCHEMA)

        return RecommendationWarningExpression(jsonData)


class ExpressionFactory():
    """
    A factory with the mechanism necessary to create expression objects of whatever type is required. The class
    returned from this class may be any child of the `Expression` class
    """

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

    @staticmethod
    def buildAndGetExpression(jsonData):
        """
        Returns an expression object 

        Args:
            jsonData: A parsed JSON expression to be validated for this class
        Returns:
            expression (Expression): An expression which is a child of the `Expression` class
        """

        expressionClass = ExpressionFactory.EXPRESSION_TYPE_MAP[jsonData["expressionType"]]
        expression = expressionClass.buildAndGetExpression(jsonData)
        return expression