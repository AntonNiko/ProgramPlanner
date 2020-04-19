from data import Data
from expression import Expression

"""
This class provides the functionality to check if a requirement is satisfied.
"""
class RequirementManager():

    def __init__(self):
        pass

    @staticmethod
    def getAcademicWritingRequirements():
        awrGroup = "uvic_references"
        awrIdentifier = "ACADEMIC_WRITING_REQUIREMENT"

        return Data.getData(awrGroup, awrIdentifier)

    @staticmethod
    def getMinimumCourseworkUnits():
        minimumCourseworkGroup = "uvic_references"
        minimumCourseworkIdentifier = "MINIMUM_COURSEWORK_UNITS"

        return Data.getData(minimumCourseworkGroup, minimumCourseworkIdentifier)

    @staticmethod
    def isRequirementSatisfied(activeTerms, requirement):
        for expression in requirement:
            assert type(expression) == Expression 

        # Check if each expression is satisfied. If not satisfied, then exception?
        for expression in requirement:
            if not expression.isExpressionSatisfied(activeTerms):
                pass
