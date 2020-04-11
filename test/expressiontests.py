import sys
sys.path.append('..')

import datetime
from expression import *
import jsonschema
from term import TermTypes
import unittest 
from unittest.mock import Mock
from utils import ThresholdType

class ReferenceExpressionTests(unittest.TestCase):
    pass


class CourseExpressionTests(unittest.TestCase):
    
    def testValidCoursePrerequisite(self):
        jsonExpression = {
            "expressionType": "COURSE",
            "code": "CSC 360",
            "requisiteType": "P"
        }

        expression = CourseExpression.buildAndGetExpression(jsonExpression)

        self.assertEqual(ExpressionType.COURSE, expression.expressionType)
        self.assertEqual("CSC 360", expression.courseCode)
        self.assertEqual(RequisiteType.PREREQUISITE, expression.requisiteType)

    def testValidCourseCorequisite(self):
        jsonExpression = {
            "expressionType": "COURSE",
            "code": "SENG 480B",
            "requisiteType": "C"
        }

        expression = CourseExpression.buildAndGetExpression(jsonExpression)

        self.assertEqual(ExpressionType.COURSE, expression.expressionType)
        self.assertEqual("SENG 480B", expression.courseCode)
        self.assertEqual(RequisiteType.COREQUISITE, expression.requisiteType)      

    def testValidCourseNoRequisite(self):  
        jsonExpression = {
            "expressionType": "COURSE",
            "code": "ENGR 120",
        }

        expression = CourseExpression.buildAndGetExpression(jsonExpression)

        self.assertEqual(ExpressionType.COURSE, expression.expressionType)
        self.assertEqual("ENGR 120", expression.courseCode)
        self.assertEqual(RequisiteType.COREQUISITE, expression.requisiteType)

    def testInvalidCourseNoCode(self):
        jsonExpression = {
            "expressionType": "COURSE",
            "requisiteType": "C"
        }     

        self.assertRaises(jsonschema.exceptions.ValidationError, CourseExpression.buildAndGetExpression, jsonExpression)   

    def testExpressionSatisfiedValidTermsPrerequisite(self):
        termOneMock = Mock()
        termOneMock.getActiveCoursesCodes.return_value = ["CSC 115", "CSC 225"]
        termTwoMock = Mock()
        termTwoMock.getActiveCoursesCodes.return_value = ["CSC 226", "SENG 350", "SENG 360"]

        activeTerms = {
            2017: {
                TermTypes.FALL_TERM: termOneMock
            },
            2018: {
                TermTypes.SPRING_TERM: termTwoMock
            }
        }

        jsonExpression = {
            "expressionType": "COURSE",
            "code": "CSC 225",
            "requisiteType": "P"
        }

        expression = CourseExpression.buildAndGetExpression(jsonExpression)
        self.assertTrue(expression.isExpressionSatisfied(activeTerms))

    def testExpressionSatisfiedValidTermsCorequisite(self):
        termOneMock = Mock()
        termOneMock.getActiveCoursesCodes.return_value = ["CSC 115", "CSC 225"]
        termTwoMock = Mock()
        termTwoMock.getActiveCoursesCodes.return_value = ["CSC 226", "SENG 350", "SENG 360"]

        activeTerms = {
            2017: {
                TermTypes.SUMMER_TERM: termOneMock,
                TermTypes.FALL_TERM: termTwoMock
            }
        }

        jsonExpression = {
            "expressionType": "COURSE",
            "code": "CSC 226",
            "requisiteType": "C"
        }

        expression = CourseExpression.buildAndGetExpression(jsonExpression)
        self.assertTrue(expression.isExpressionSatisfied(activeTerms))

    def testExpressionSatisfiedValidTermsPrerequisiteUnsatisfied(self):
        termOneMock = Mock()
        termOneMock.getActiveCoursesCodes.return_value = ["CSC 115", "CSC 225"]
        termTwoMock = Mock()
        termTwoMock.getActiveCoursesCodes.return_value = ["CSC 226", "SENG 350", "SENG 360"]  

        activeTerms = {
            2017: {
                TermTypes.FALL_TERM: termOneMock
            },
            2018: {
                TermTypes.SPRING_TERM: termTwoMock
            }
        }

        jsonExpression = {
            "expressionType": "COURSE",
            "code": "CSC 226",
            "requisiteType": "P"
        }

        expression = CourseExpression.buildAndGetExpression(jsonExpression)
        self.assertFalse(expression.isExpressionSatisfied(activeTerms))             


class ConditionalExpressionTests(unittest.TestCase):

    def testValidExpressionCoursesOrCondition(self):
        jsonExpression = {
            "expressionType": "CONDITIONAL",
            "expressionOne": {
                "expressionType": "COURSE",
                "code": "CSC 320",
                "requisiteType": "P"
            },
            "expressionTwo": {
                "expressionType": "COURSE",
                "code": "CSC 360",
                "requisiteType": "C"
            },
            "condition": "OR"
        }

        expression = ConditionalExpression.buildAndGetExpression(jsonExpression)

        self.assertEqual(ExpressionType.CONDITIONAL, expression.expressionType)
        self.assertEqual(CourseExpression, type(expression.expressionOne.expression))
        self.assertEqual(CourseExpression, type(expression.expressionTwo.expression))
        self.assertEqual(ConditionType.OR, expression.condition)

    def testValidExpressionCoursesAndCondition(self):
        jsonExpression = {
            "expressionType": "CONDITIONAL",
            "expressionOne": {
                "expressionType": "COURSE",
                "code": "SENG 480A",
            },
            "expressionTwo": {
                "expressionType": "COURSE",
                "code": "CSC 370",
                "requisiteType": "C"
            },
            "condition": "AND"
        }

        expression = ConditionalExpression.buildAndGetExpression(jsonExpression)

        self.assertEqual(ExpressionType.CONDITIONAL, expression.expressionType)
        self.assertEqual(CourseExpression, type(expression.expressionOne.expression))
        self.assertEqual(CourseExpression, type(expression.expressionTwo.expression))
        self.assertEqual(ConditionType.AND, expression.condition)  

    def testInvalidExpressionNoCondition(self):
        jsonExpression = {
            "expressionType": "CONDITIONAL",
            "expressionOne": {
                "expressionType": "COURSE",
                "code": "SENG 480A",
            },
            "expressionTwo": {
                "expressionType": "COURSE",
                "code": "CSC 370",
                "requisiteType": "C"
            }
        }     

        self.assertRaises(jsonschema.exceptions.ValidationError, ConditionalExpression.buildAndGetExpression, jsonExpression)


class ListExpressionTests(unittest.TestCase):

    def testValidExpressionListOfCoursesGeq(self):
        jsonExpression = {
            "expressionType": "LIST",
            "threshold": 1,
            "type": "geq",
            "expressions": [{
                "expressionType": "COURSE",
                "code": "ENGR 110",
                "requisiteType": "P"
            },
            {
                "expressionType": "COURSE",
                "code": "ENGR 111",
                "requisiteType": "C"
            },
            {
                "expressionType": "COURSE",
                "code": "ENGR 112",
                "requisiteType": "P"
            }]
        }

        expression = ListExpression.buildAndGetExpression(jsonExpression)

        self.assertEqual(ExpressionType.LIST, expression.expressionType)
        self.assertEqual(1, expression.threshold)
        self.assertEqual(ThresholdType.GREATER_THAN_OR_EQUAL, expression.type)
        self.assertEqual(list, type(expression.expressions))
        for e in expression.expressions:
            self.assertEqual(CourseExpression, type(e.expression))

    def testValidExpressionListOfCoursesLeq(self):
        jsonExpression = {
            "expressionType": "LIST",
            "threshold": 2,
            "type": "leq",
            "expressions": [{
                "expressionType": "COURSE",
                "code": "MATH 122",
                "requisiteType": "C"
            },
            {
                "expressionType": "COURSE",
                "code": "MATH 200",
                "requisiteType": "P"
            }
            ]
        }

        expression = ListExpression.buildAndGetExpression(jsonExpression)

        self.assertEqual(ExpressionType.LIST, expression.expressionType)
        self.assertEqual(2, expression.threshold)
        self.assertEqual(ThresholdType.LESS_THAN_OR_EQUAL, expression.type)
        self.assertEqual(list, type(expression.expressions))
        for e in expression.expressions:
            self.assertEqual(CourseExpression, type(e.expression))

    def testInvalidExpressionThresholdOutofRangeNegative(self):
        jsonExpression = {
            "expressionType": "LIST",
            "threshold": -1,
            "type": "leq",
            "expressions": [{
                "expressionType": "COURSE",
                "code": "MATH 122",
                "requisiteType": "C"
            },
            {
                "expressionType": "COURSE",
                "code": "MATH 200",
                "requisiteType": "P"
            }
            ]
        }

        self.assertRaises(AssertionError, ListExpression.buildAndGetExpression, jsonExpression)

    def testInvalidExpressionThresholdOutofRangePositive(self):
        jsonExpression = {
            "expressionType": "LIST",
            "threshold": 3,
            "type": "leq",
            "expressions": [{
                "expressionType": "COURSE",
                "code": "MATH 122",
                "requisiteType": "C"
            },
            {
                "expressionType": "COURSE",
                "code": "MATH 200",
                "requisiteType": "P"
            }
            ]
        }

        self.assertRaises(AssertionError, ListExpression.buildAndGetExpression, jsonExpression)



class ExpressionTests(unittest.TestCase):
    
    def testValidExpressionList(self):
        pass
