import sys
sys.path.append('..')

import datetime
from schedule import *
import unittest

class SectionTests(unittest.TestCase):
    
    def testConstructorValidData(self):
        jsonData = {
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
        }

        section = Section(jsonData)

        self.assertEqual("A01", section.name) 
        self.assertEqual(SectionType.LECTURE, section.type)
        self.assertEqual(31466, section.crn)
        self.assertEqual(1, len(section.meetings))
        self.assertEqual(SectionMeeting, type(section.meetings[0]))

class SectionMeetingTests(unittest.TestCase):

    def testConstructorValidData(self):
        jsonData = {
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

        meeting = SectionMeeting(jsonData)

        self.assertEqual(list, type(meeting.days))
        self.assertEqual(1, len(meeting.days))
        self.assertEqual(WeekdayString.TUESDAY, meeting.days[0])
        self.assertEqual("ECS 125", meeting.location)

        self.assertEqual(datetime.date(2020, 6, 5), meeting.dates["start"])
        self.assertEqual(datetime.date(2020, 7, 31), meeting.dates["end"])
        self.assertEqual(datetime.time(14, 30), meeting.times["start"])
        self.assertEqual(datetime.time(16, 20), meeting.times["end"])

    def testDoesMeetingConflict(self):
        jsonDataOne = {
                    "days": ["T", "W", "F"],
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

        jsonDataTwo = {
                    "days": ["M", "W", "R"],
                    "location": "ECS 123",
                    "date range": {
                        "start": "2020-06-05",
                        "end":   "2020-07-31"
                    },
                    "times": {
                        "start": "14:30",
                        "end":   "16:20"
                    }
        }

    def testGetWeekdaysInDateRangeValidThreeDaySpan(self):
        dateOne = datetime.date(2020, 8, 18)
        dateTwo = datetime.date(2020, 8, 21)

        expectedResult = [Weekday.TUESDAY, Weekday.WEDNESDAY, Weekday.THURSDAY, Weekday.FRIDAY]
        actualResult = SectionMeeting.getWeekdaysInDateRange(dateOne, dateTwo)
        self.assertListEqual(expectedResult, actualResult)

    def testDoesTimeConflictConflictingTimes(self):
        timeOne = {
            "start": datetime.time(10, 20),
            "end": datetime.time(16, 30)
        }

        timeTwo = {
            "start": datetime.time(16, 00),
            "end": datetime.time(18, 00)
        } 

        self.assertTrue(SectionMeeting.doesTimeConflict(timeOne, timeTwo))

    def testDoesTimeConflictNonConflictingTimes(self):
        timeOne = {
            "start": datetime.time(10, 20),
            "end": datetime.time(11, 30)
        }

        timeTwo = {
            "start": datetime.time(11, 40),
            "end": datetime.time(18, 00)
        } 

        self.assertFalse(SectionMeeting.doesTimeConflict(timeOne, timeTwo))

    def testDoesTimeConflictEqualStartEndTimes(self):
        timeOne = {
            "start": datetime.time(10, 20),
            "end": datetime.time(11, 30)
        }

        timeTwo = {
            "start": datetime.time(11, 30),
            "end": datetime.time(12, 20)
        } 

        self.assertFalse(SectionMeeting.doesTimeConflict(timeOne, timeTwo))

if __name__ == "__main__":
    unittest.main()