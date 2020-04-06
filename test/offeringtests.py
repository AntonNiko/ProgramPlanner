import sys
sys.path.append('..')

from course import CourseCode, CourseDetails, UVicCourseDetails
from institution import Institution
from offering import OfferingCourse
from requirement import Requirement
from schedule import Section
import unittest


class OfferingCourseTests(unittest.TestCase):
    
    def testConstructorValidParameters(self):
        institution = Institution.UNIVERSITY_OF_VICTORIA
        courseCode = CourseCode("ENGR 110")
        name = "Design and Communication I"
        credits = 2.5
        requirements = Requirement(None)
        details = UVicCourseDetails(4.0, 2.0, 0.0, None)
        sections = [
            Section({
                "name": "A01",
                "type": "lecture",
                "crn" : 31466,
                "meetings": [
                    {
                        "days": ["T"],
                        "location": "ECS 125",
                        "date range": {
                            "start": "2020-06-05",
                            "end":   "2020-07-31"
                        },
                        "times": {
                            "start": "14:30",
                            "end":   "16:20"
                        }
                    }
                ]
            })
        ]

        offering = OfferingCourse(institution, courseCode, name, credits, requirements, details, sections)

        self.assertEqual(Institution.UNIVERSITY_OF_VICTORIA, offering.institution)
        self.assertEqual(CourseCode("ENGR 110"), offering.courseCode)
        self.assertEqual("Design and Communication I", offering.name)
        self.assertEqual(2.5, offering.credits)
        #TODO: Requirement validation
        #TODO: Course Details validation ? maybe not here
        self.assertDictEqual({"A01": sections[0]}, offering.sections)

    def testDoesSectionConflictConflictingSection(self):
        institution = Institution.UNIVERSITY_OF_VICTORIA
        courseCode = CourseCode("ENGR 110")
        name = "Design and Communication I"
        credits = 2.5
        requirements = Requirement(None)
        details = UVicCourseDetails(4.0, 2.0, 0.0, None)
        sections = [
            Section({
                "name": "A01",
                "type": "lecture",
                "crn" : 31466,
                "meetings": [
                    {
                        "days": ["T"],
                        "location": "ECS 125",
                        "date range": {
                            "start": "2020-06-05",
                            "end":   "2020-07-31"
                        },
                        "times": {
                            "start": "14:30",
                            "end":   "16:20"
                        }
                    }
                ]
            })
        ]
        offering = OfferingCourse(institution, courseCode, name, credits, requirements, details, sections)

        sectionToTest = Section({
            "name": "A01",
            "type": "lecture",
            "crn" : 31466,
            "meetings": [
                {
                    "days": ["M","T","W"],
                    "location": "ECS 125",
                    "date range": {
                        "start": "2020-06-05",
                        "end":   "2020-07-31"
                    },
                    "times": {
                        "start": "13:30",
                        "end":   "14:50"
                    }
                }
            ]
        })

        self.assertTrue(offering.doesSectionConflict(sectionToTest))

    def testDoesSectionConflictConflictingListSections(self):
        institution = Institution.UNIVERSITY_OF_VICTORIA
        courseCode = CourseCode("ENGR 110")
        name = "Design and Communication I"
        credits = 2.5
        requirements = Requirement(None)
        details = UVicCourseDetails(4.0, 2.0, 0.0, None)
        sections = [
            Section({
                "name": "A01",
                "type": "lecture",
                "crn" : 31466,
                "meetings": [
                    {
                        "days": ["T"],
                        "location": "ECS 125",
                        "date range": {
                            "start": "2020-06-05",
                            "end":   "2020-07-31"
                        },
                        "times": {
                            "start": "14:30",
                            "end":   "16:20"
                        }
                    }
                ]
            }),
            Section({
                "name": "B01",
                "type": "lab",
                "crn" : 31490,
                "meetings": [
                    {
                        "days": ["R","F"],
                        "location": "HSD A240",
                        "date range": {
                            "start": "2020-06-05",
                            "end":   "2020-07-31"
                        },
                        "times": {
                            "start": "14:30",
                            "end":   "16:20"
                        }
                    }
                ]
            })
        ]
        offering = OfferingCourse(institution, courseCode, name, credits, requirements, details, sections)

        sectionToTest = Section({
            "name": "A01",
            "type": "lecture",
            "crn" : 32499,
            "meetings": [
                {
                    "days": ["M","T","W"],
                    "location": "ECS 125",
                    "date range": {
                        "start": "2020-06-05",
                        "end":   "2020-07-31"
                    },
                    "times": {
                        "start": "13:30",
                        "end":   "14:50"
                    }
                }
            ]
        })

        self.assertTrue(offering.doesSectionConflict(sectionToTest))
        self.assertFalse(offering.doesSectionConflict(sectionToTest, "B01"))