from expression import Expression

"""
This class provides the functionality to check if a requirement is satisfied.
"""
class RequirementManager():

    def __init__(self):
        pass

    """
    A requirement is a list of expressions. 
    """
    def isRequirementSatisfied(self, activeTerms, requirement):
        for expression in requirement:
            assert type(expression) == Expression 

        # Check if each expression is satisfied. If not satisfied, then exception?
        for expression in requirement:
            if not expression.isExpressionSatisfied(activeTerms):
                pass
