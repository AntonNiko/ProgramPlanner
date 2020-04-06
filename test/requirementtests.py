import sys
sys.path.append('..')

from requirement import *
import unittest 


class ExpressionTests(unittest.TestCase):
    
    def testValidExpressionList(self):
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

class ConditionalExpressionTests(unittest.TestCase):

    def testValidExpressionOrCondition(self):
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
        self.assertEqual(CourseExpression, type(expression.expressionOne))
        self.assertEqual(CourseExpression, type(expression.expressionTwo))
        self.assertEqual(ConditionType.OR, expression.condition)

class ListExpressionTests(unittest.TestCase):

    def testValidExpressionListOfCourses(self):
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
        self.assertEqual("geq", expression.type)
        self.assertEqual(list, type(expression.expressions))
        for e in expression.expressions:
            self.assertEqual(CourseExpression, type(e))