import sys
sys.path.append('..')

import datetime
from expression import *
import json
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
            "requisiteType": "P",
            "message": "CSC 360"
        }

        expression = CourseExpression.buildAndGetExpression(jsonExpression)

        self.assertEqual(ExpressionType.COURSE, expression.expressionType)
        self.assertEqual("CSC 360", expression.courseCode)
        self.assertEqual(RequisiteType.PREREQUISITE, expression.requisiteType)
        self.assertEqual("CSC 360", expression.message)

    def testValidCourseCorequisite(self):
        jsonExpression = {
            "expressionType": "COURSE",
            "code": "SENG 480B",
            "requisiteType": "C",
            "message": "SENG 480B"
        }

        expression = CourseExpression.buildAndGetExpression(jsonExpression)

        self.assertEqual(ExpressionType.COURSE, expression.expressionType)
        self.assertEqual("SENG 480B", expression.courseCode)
        self.assertEqual(RequisiteType.COREQUISITE, expression.requisiteType)
        self.assertEqual("SENG 480B", expression.message)      

    def testValidCourseNoRequisite(self):  
        jsonExpression = {
            "expressionType": "COURSE",
            "code": "ENGR 120"
        }

        expression = CourseExpression.buildAndGetExpression(jsonExpression)

        self.assertEqual(ExpressionType.COURSE, expression.expressionType)
        self.assertEqual("ENGR 120", expression.courseCode)
        self.assertEqual(RequisiteType.COREQUISITE, expression.requisiteType)
        self.assertEqual(None, expression.message)

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
            "requisiteType": "P",
            "message": "CSC 225"
        }

        expression = CourseExpression.buildAndGetExpression(jsonExpression)
        result = expression.isExpressionSatisfied(activeTerms)
        
        self.assertTrue(result.satisfied)
        self.assertCountEqual([{"message": "CSC 225", "isSatisfied": True}], result.expressionStatus)

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
            "requisiteType": "C",
            "message": None
        }

        expression = CourseExpression.buildAndGetExpression(jsonExpression)
        result = expression.isExpressionSatisfied(activeTerms)
        
        self.assertTrue(result.satisfied)
        self.assertListEqual([], result.expressionStatus)

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
            "requisiteType": "P",
            "message": "CSC 226"
        }

        expression = CourseExpression.buildAndGetExpression(jsonExpression)
        result = expression.isExpressionSatisfied(activeTerms)
        
        self.assertFalse(result.satisfied)
        self.assertCountEqual([{"message": "CSC 226", "isSatisfied": False}], result.expressionStatus)        


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
            "condition": "OR",
            "message": "CSC 320 or CSC 360"
        }

        expression = ConditionalExpression.buildAndGetExpression(jsonExpression)

        self.assertEqual(ExpressionType.CONDITIONAL, expression.expressionType)
        self.assertEqual(CourseExpression, type(expression.expressionOne))
        self.assertEqual(CourseExpression, type(expression.expressionTwo))
        self.assertEqual(ConditionType.OR, expression.condition)
        self.assertEqual("CSC 320 or CSC 360", expression.message)

    def testValidExpressionCoursesAndCondition(self):
        jsonExpression = {
            "expressionType": "CONDITIONAL",
            "expressionOne": {
                "expressionType": "COURSE",
                "code": "SENG 480A"
            },
            "expressionTwo": {
                "expressionType": "COURSE",
                "code": "CSC 370",
                "requisiteType": "C"
            },
            "condition": "AND",
            "message": "SENG 480A or CSC 370"
        }

        expression = ConditionalExpression.buildAndGetExpression(jsonExpression)

        self.assertEqual(ExpressionType.CONDITIONAL, expression.expressionType)
        self.assertEqual(CourseExpression, type(expression.expressionOne))
        self.assertEqual(CourseExpression, type(expression.expressionTwo))
        self.assertEqual(ConditionType.AND, expression.condition)  
        self.assertEqual("SENG 480A or CSC 370", expression.message)

    def testInvalidExpressionNoCondition(self):
        jsonExpression = {
            "expressionType": "CONDITIONAL",
            "expressionOne": {
                "expressionType": "COURSE",
                "code": "SENG 480A"
            },
            "expressionTwo": {
                "expressionType": "COURSE",
                "code": "CSC 370",
                "requisiteType": "C"
            },
            "message": "SENG 480A or CSC 370"
        }     

        self.assertRaises(jsonschema.exceptions.ValidationError, ConditionalExpression.buildAndGetExpression, jsonExpression)

    def testExpressionSatisfiedValidCoursesOrCondition(self):
        termOneMock = Mock()
        termOneMock.getActiveCoursesCodes.return_value = ["CSC 115", "CSC 225", "ENGR 120", "ECON 180"]
        termTwoMock = Mock()
        termTwoMock.getActiveCoursesCodes.return_value = ["CSC 226", "SENG 350", "SENG 480B", "SENG 275"]  

        activeTerms = {
            2017: {
                TermTypes.FALL_TERM: termOneMock
            },
            2018: {
                TermTypes.SPRING_TERM: termTwoMock
            }
        }

        jsonExpression = {
            "expressionType": "CONDITIONAL",
            "expressionOne": {
                "expressionType": "COURSE",
                "code": "CSC 115",
                "requisiteType": "P"
            },
            "expressionTwo": {
                "expressionType": "COURSE",
                "code": "CSC 116",
                "requisiteType": "P"
            },
            "condition": "OR",
            "message": "CSC 115 or CSC 116"
        }

        expression = ConditionalExpression.buildAndGetExpression(jsonExpression)
        result = expression.isExpressionSatisfied(activeTerms)
        
        self.assertTrue(result.satisfied)
        self.assertCountEqual([{"message": "CSC 115 or CSC 116", "isSatisfied": True}], result.expressionStatus)  

    def testExpressionSatisfiedValidCoursesAndCondition(self):
        termOneMock = Mock()
        termOneMock.getActiveCoursesCodes.return_value = ["CSC 320", "CSC 360", "ENGR 297", "SENG 475"]
        termTwoMock = Mock()
        termTwoMock.getActiveCoursesCodes.return_value = ["CSC 349A", "SENG 350", "SENG 480B", "SENG 275"]  

        activeTerms = {
            2017: {
                TermTypes.FALL_TERM: termOneMock
            },
            2018: {
                TermTypes.SPRING_TERM: termTwoMock
            }
        }

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
                "requisiteType": "P"
            },
            "condition": "AND",
            "message": "CSC 320 and CSC 360"
        }  

        expression = ConditionalExpression.buildAndGetExpression(jsonExpression)
        result = expression.isExpressionSatisfied(activeTerms)
        
        self.assertTrue(result.satisfied)
        self.assertCountEqual([{"message": "CSC 320 and CSC 360", "isSatisfied": True}], result.expressionStatus) 

    def testExpressionSatisfiedValidCourseOrConditonUnsatisfied(self):
        termOneMock = Mock()
        termOneMock.getActiveCoursesCodes.return_value = ["CSC 320", "CSC 360", "ENGR 297", "SENG 475"]
        termTwoMock = Mock()
        termTwoMock.getActiveCoursesCodes.return_value = ["CSC 349A", "SENG 360", "SENG 480B", "SENG 275"]  

        activeTerms = {
            2017: {
                TermTypes.FALL_TERM: termOneMock
            },
            2018: {
                TermTypes.SPRING_TERM: termTwoMock
            }
        }

        jsonExpression = {
            "expressionType": "CONDITIONAL",
            "expressionOne": {
                "expressionType": "COURSE",
                "code": "CSC 399",
                "requisiteType": "P"
            },
            "expressionTwo": {
                "expressionType": "COURSE",
                "code": "SENG 350",
                "requisiteType": "P",
                "message": "SENG 350"
            },
            "condition": "OR",
            "message": "CSC 399 or SENG 350"
        }  

        expression = ConditionalExpression.buildAndGetExpression(jsonExpression)
        result = expression.isExpressionSatisfied(activeTerms)
        
        self.assertFalse(result.satisfied)
        self.assertCountEqual([{"message": "CSC 399 or SENG 350", "isSatisfied": False}, {"message": "SENG 350", "isSatisfied": False}], result.expressionStatus)

    def testExpressionSatisfiedValidCourseOrConditionUnsatisfiedPrerequisite(self):
        termOneMock = Mock()
        termOneMock.getActiveCoursesCodes.return_value = ["CSC 320", "CSC 360", "ENGR 297", "SENG 475"]
        termTwoMock = Mock()
        termTwoMock.getActiveCoursesCodes.return_value = ["CSC 399", "SENG 350", "SENG 480B", "SENG 275"]  

        activeTerms = {
            2017: {
                TermTypes.FALL_TERM: termOneMock
            },
            2018: {
                TermTypes.SPRING_TERM: termTwoMock
            }
        }

        jsonExpression = {
            "expressionType": "CONDITIONAL",
            "expressionOne": {
                "expressionType": "COURSE",
                "code": "CSC 399",
                "requisiteType": "P"
            },
            "expressionTwo": {
                "expressionType": "COURSE",
                "code": "SENG 350",
                "requisiteType": "P"
            },
            "condition": "OR",
            "message": "CSC 399 or SENG 350"
        }      

        expression = ConditionalExpression.buildAndGetExpression(jsonExpression)
        result = expression.isExpressionSatisfied(activeTerms)
        
        self.assertFalse(result.satisfied)
        self.assertCountEqual([{"message": "CSC 399 or SENG 350", "isSatisfied": False}], result.expressionStatus) 

    def testExpressionSatisfiedValidCourseAndConditionUnsatisfiedPrerequisite(self):
        termOneMock = Mock()
        termOneMock.getActiveCoursesCodes.return_value = ["CSC 320", "CSC 360", "ENGR 297", "SENG 475"]
        termTwoMock = Mock()
        termTwoMock.getActiveCoursesCodes.return_value = ["CSC 399", "SENG 350", "SENG 480B", "SENG 275"]  

        activeTerms = {
            2017: {
                TermTypes.FALL_TERM: termOneMock
            },
            2018: {
                TermTypes.SPRING_TERM: termTwoMock
            }
        }

        jsonExpression = {
            "expressionType": "CONDITIONAL",
            "expressionOne": {
                "expressionType": "COURSE",
                "code": "CSC 399",
                "requisiteType": "P"
            },
            "expressionTwo": {
                "expressionType": "COURSE",
                "code": "CSC 360",
                "requisiteType": "C"
            },
            "condition": "AND",
            "message": "CSC 399 or CSC 360"
        }                 

        expression = ConditionalExpression.buildAndGetExpression(jsonExpression)
        result = expression.isExpressionSatisfied(activeTerms)

        self.assertFalse(result.satisfied)
        self.assertCountEqual([{"message": "CSC 399 or CSC 360", "isSatisfied": False}], result.expressionStatus)


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
            }],
            "message": "One of ENGR 110, ENGR 111, or ENGR 112"
        }

        expression = ListExpression.buildAndGetExpression(jsonExpression)

        self.assertEqual(ExpressionType.LIST, expression.expressionType)
        self.assertEqual(1, expression.threshold)
        self.assertEqual(ThresholdType.GREATER_THAN_OR_EQUAL, expression.type)
        self.assertEqual(list, type(expression.expressions))
        for e in expression.expressions:
            self.assertEqual(CourseExpression, type(e))

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
            }],
            "message": "At least 2 of MATH 122 or MATH 200"
        }

        expression = ListExpression.buildAndGetExpression(jsonExpression)

        self.assertEqual(ExpressionType.LIST, expression.expressionType)
        self.assertEqual(2, expression.threshold)
        self.assertEqual(ThresholdType.LESS_THAN_OR_EQUAL, expression.type)
        self.assertEqual(list, type(expression.expressions))
        for e in expression.expressions:
            self.assertEqual(CourseExpression, type(e))

    def testExpressionSatisfiedValidListOfCoursesGeqSatisfied(self):
        termOneMock = Mock()
        termOneMock.getActiveCoursesCodes.return_value = ["MECH 200"]
        termTwoMock = Mock()
        termTwoMock.getActiveCoursesCodes.return_value = ["MECH 285", "MECH 220"] 
        termThreeMock = Mock() 
        termThreeMock.getActiveCoursesCodes.return_value = ["CSC 399", "SENG 350", "SENG 480B", "SENG 275"] 

        activeTerms = {
            2017: {
                TermTypes.FALL_TERM: termOneMock
            },
            2018: {
                TermTypes.SPRING_TERM: termTwoMock,
                TermTypes.SUMMER_TERM: termThreeMock
            }
        }

        jsonExpression = {
            "expressionType": "LIST",
            "threshold": 1,
            "type": "geq",
            "expressions": [{
                "expressionType": "COURSE",
                "code": "MECH 200",
                "requisiteType": "P",
                "message": "MECH 200"
            },
            {
                "expressionType": "COURSE",
                "code": "ECE 299",
                "requisiteType": "P"
            },
            {
                "expressionType": "COURSE",
                "code": "ELEC 299",
                "requisiteType": "P",
                "message": "ELEC 299"
            }],
            "message": "One of MECH 200, ECE 299, ELEC 299"
        }

        expression = ListExpression.buildAndGetExpression(jsonExpression)
        result = expression.isExpressionSatisfied(activeTerms)

        self.assertTrue(result.satisfied)
        self.assertCountEqual([{"message": "One of MECH 200, ECE 299, ELEC 299", "isSatisfied": True}, {"message": "MECH 200", "isSatisfied": True}, {"message": "ELEC 299", "isSatisfied": False}], result.expressionStatus)
        
    def testExpressionSatisfiedValidListOfExpressionsGtSatisfied(self):
        termOneMock = Mock()
        termOneMock.getActiveCoursesCodes.return_value = ["MECH 200"]
        termTwoMock = Mock()
        termTwoMock.getActiveCoursesCodes.return_value = ["ELEC 299", "MECH 220"] 
        termThreeMock = Mock() 
        termThreeMock.getActiveCoursesCodes.return_value = ["CSC 360", "SENG 350", "SENG 480B", "SENG 275"] 

        activeTerms = {
            2017: {
                TermTypes.FALL_TERM: termOneMock
            },
            2018: {
                TermTypes.SPRING_TERM: termTwoMock,
                TermTypes.SUMMER_TERM: termThreeMock
            }
        }

        jsonExpression = {
            "expressionType": "LIST",
            "threshold": 1,
            "type": "gt",
            "expressions": [{
                "expressionType": "CONDITIONAL",
                "expressionOne": {
                    "expressionType": "COURSE",
                    "code": "CSC 399",
                    "requisiteType": "P"
                },
                "expressionTwo": {
                    "expressionType": "COURSE",
                    "code": "CSC 360",
                    "requisiteType": "C"
                },
                "condition": "OR",
                "message": "CSC 399 or CSC 360"
            },
            {
                "expressionType": "COURSE",
                "code": "ECE 299",
                "requisiteType": "P"
            },
            {
                "expressionType": "COURSE",
                "code": "ELEC 299",
                "requisiteType": "P",
                "message": "ELEC 299"
            }],
            "message": "At least two of some courses"
        }

        expression = ListExpression.buildAndGetExpression(jsonExpression)
        result = expression.isExpressionSatisfied(activeTerms)

        self.assertTrue(result.satisfied)
        self.assertCountEqual([{"message": "At least two of some courses", "isSatisfied": True}, {"message": "CSC 399 or CSC 360", "isSatisfied": True}, {"message": "ELEC 299", "isSatisfied": True}], result.expressionStatus)

    def testExpressionSatisfiedValidListOfExpressionsGeqUnsatisfied(self):
        termOneMock = Mock()
        termOneMock.getActiveCoursesCodes.return_value = ["MECH 200"]
        termTwoMock = Mock()
        termTwoMock.getActiveCoursesCodes.return_value = ["ECE 260", "MECH 220"] 
        termThreeMock = Mock() 
        termThreeMock.getActiveCoursesCodes.return_value = ["CSC 360", "SENG 350", "SENG 480B", "SENG 275"] 

        activeTerms = {
            2017: {
                TermTypes.FALL_TERM: termOneMock
            },
            2018: {
                TermTypes.SPRING_TERM: termTwoMock,
                TermTypes.SUMMER_TERM: termThreeMock
            }
        }

        jsonExpression = {
            "expressionType": "LIST",
            "threshold": 1,
            "type": "gt",
            "expressions": [
            {
                "expressionType": "COURSE",
                "code": "ECE 360",
                "requisiteType": "C"
            },
            {
                "expressionType": "COURSE",
                "code": "ECE 299",
                "requisiteType": "P"
            },
            {
                "expressionType": "COURSE",
                "code": "ELEC 299",
                "requisiteType": "P",
            }],
            "message": "At least two of some courses"
        }

        expression = ListExpression.buildAndGetExpression(jsonExpression)
        result = expression.isExpressionSatisfied(activeTerms)

        self.assertFalse(result.satisfied)
        self.assertCountEqual([{"message": "At least two of some courses", "isSatisfied": False}], result.expressionStatus)


class ExpressionFactoryTests(unittest.TestCase):
    """
    The tests for this class are meant to assert that the JSON expressions map to the correct class.
    """
    
    def testValidExpressionList(self):
        pass
