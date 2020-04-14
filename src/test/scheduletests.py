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
        self.assertEqual(Weekday.TUESDAY, meeting.days[0])
        self.assertEqual("ECS 125", meeting.location)

        self.assertEqual(datetime.date(2020, 6, 5), meeting.dates["start"])
        self.assertEqual(datetime.date(2020, 7, 31), meeting.dates["end"])
        self.assertEqual(datetime.time(14, 30), meeting.times["start"])
        self.assertEqual(datetime.time(16, 20), meeting.times["end"]) 

    def testDoesMeetingConflictConflictingMeetings(self):
        meetingOne = {
                    "days": ["M", "R"],
                    "location": "ECS 123",
                    "date range": {
                        "start": "2020-05-04",
                        "end":   "2020-07-31"
                    },
                    "times": {
                        "start": "10:00",
                        "end":   "11:20"
                    }
        }

        meetingTwo = {
                    "days": ["M", "W", "F"],
                    "location": "ECS 125",
                    "date range": {
                        "start": "2020-05-04",
                        "end":   "2020-07-31"
                    },
                    "times": {
                        "start": "10:30",
                        "end":   "12:00"
                    }
        }

        sectionMeetingOne = SectionMeeting(meetingOne)
        sectionMeetingTwo = SectionMeeting(meetingTwo)

        self.assertTrue(sectionMeetingOne.doesMeetingConflict(sectionMeetingTwo))

    def testDoesMeetingConflictNonConflictingMeetingsLessThanSevenDays(self):
        # This tests the behavior of overlapping meetings. In this case,
        # overlaps by 3 days.
        # 
        #  Day     |  Jun 16 | Jun 17  |  Jun 18  |
        #  Weekday |   Wed   |  Thu    |    Fri   |
        #  Meet. 1 |         |    X    |          |
        #  Meet. 2 |    X    |         |     X    |
        #
        # No times actually overlap. Therefore we expect no conflicts
        
        meetingOne = {
                    "days": ["M", "R"],
                    "location": "ECS 123",
                    "date range": {
                        "start": "2020-05-04",
                        "end":   "2020-06-18"
                    },
                    "times": {
                        "start": "10:00",
                        "end":   "11:20"
                    }
        }

        meetingTwo = {
                    "days": ["M", "W", "F"],
                    "location": "ECS 125",
                    "date range": {
                        "start": "2020-06-16",
                        "end":   "2020-07-31"
                    },
                    "times": {
                        "start": "10:30",
                        "end":   "12:00"
                    }
        }

        sectionMeetingOne = SectionMeeting(meetingOne)
        sectionMeetingTwo = SectionMeeting(meetingTwo)

        self.assertFalse(sectionMeetingOne.doesMeetingConflict(sectionMeetingTwo))  
        #self.assertFalse(sectionMeetingTwo.doesMeetingConflict(sectionMeetingOne))      

    def testDoesMeetingConflictConflictingMeetingsLessThanSevenDays(self):
        # This tests the behavior of overlapping meetings. In this case,
        # overlaps by 3 days.
        # 
        #  Day     |  Jun 16 | Jun 17  |  Jun 18  |
        #  Weekday |   Wed   |  Thu    |    Fri   |
        #  Meet. 1 |    X    |         |          |
        #  Meet. 2 |    X    |         |     X    |
        #
        # No times actually overlap. Therefore we expect no conflicts
        
        meetingOne = {
                    "days": ["M", "W"],
                    "location": "ECS 123",
                    "date range": {
                        "start": "2020-05-04",
                        "end":   "2020-06-18"
                    },
                    "times": {
                        "start": "10:00",
                        "end":   "11:20"
                    }
        }

        meetingTwo = {
                    "days": ["M", "W", "F"],
                    "location": "ECS 125",
                    "date range": {
                        "start": "2020-06-16",
                        "end":   "2020-07-31"
                    },
                    "times": {
                        "start": "10:30",
                        "end":   "12:00"
                    }
        }

        sectionMeetingOne = SectionMeeting(meetingOne)
        sectionMeetingTwo = SectionMeeting(meetingTwo)

        self.assertTrue(sectionMeetingOne.doesMeetingConflict(sectionMeetingTwo))  
        #self.assertTrue(sectionMeetingTwo.doesMeetingConflict(sectionMeetingOne))      

    def testDoesMeetingConflictNonConflictingMeetingsSeparateDates(self):
        meetingOne = {
                    "days": ["M", "R"],
                    "location": "ECS 123",
                    "date range": {
                        "start": "2020-05-04",
                        "end":   "2020-07-31"
                    },
                    "times": {
                        "start": "10:00",
                        "end":   "11:20"
                    }
        }

        meetingTwo = {
                    "days": ["M", "W", "F"],
                    "location": "ECS 125",
                    "date range": {
                        "start": "2020-08-01",
                        "end":   "2020-08-31"
                    },
                    "times": {
                        "start": "10:30",
                        "end":   "12:00"
                    }
        }     

        sectionMeetingOne = SectionMeeting(meetingOne)
        sectionMeetingTwo = SectionMeeting(meetingTwo)

        self.assertFalse(sectionMeetingOne.doesMeetingConflict(sectionMeetingTwo))   

    def testGetWeekdaysInDateRangeValidThreeDaySpan(self):
        dateOne = datetime.date(2020, 8, 18)
        dateTwo = datetime.date(2020, 8, 21)

        expectedResult = [Weekday.TUESDAY, Weekday.WEDNESDAY, Weekday.THURSDAY, Weekday.FRIDAY]
        actualResult = SectionMeeting.getWeekdaysInDateRange(dateOne, dateTwo)
        self.assertListEqual(expectedResult, actualResult)

    def testGetWeekdaysInDateRangeValidThreeDaySpanReversed(self):
        dateOne = datetime.date(2020, 8, 21)
        dateTwo = datetime.date(2020, 8, 18)

        expectedResult = [Weekday.TUESDAY, Weekday.WEDNESDAY, Weekday.THURSDAY, Weekday.FRIDAY]
        actualResult = SectionMeeting.getWeekdaysInDateRange(dateOne, dateTwo)
        self.assertListEqual(expectedResult, actualResult)

    def testGetWeekdaysInDateRangeValidSevenDaySpan(self):
        dateOne = datetime.date(2020, 8, 19)
        dateTwo = datetime.date(2020, 8, 25)

        expectedResult = [Weekday.WEDNESDAY, Weekday.THURSDAY, Weekday.FRIDAY, Weekday.SATURDAY, Weekday.SUNDAY, Weekday.MONDAY, Weekday.TUESDAY]
        actualResult = SectionMeeting.getWeekdaysInDateRange(dateOne, dateTwo)
        self.assertListEqual(expectedResult, actualResult) 

    def testGetWeekdaysInDateRangeValidTenDaySpan(self):  
        dateOne = datetime.date(2020, 8, 17)
        dateTwo = datetime.date(2020, 8, 26)

        expectedResult = [Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY, Weekday.THURSDAY, Weekday.FRIDAY, Weekday.SATURDAY, Weekday.SUNDAY]
        actualResult = SectionMeeting.getWeekdaysInDateRange(dateOne, dateTwo)
        self.assertListEqual(expectedResult, actualResult)      

    def testDoesDateConflictConflictingDates(self):
        dateOne = {
            "start": datetime.date(2020, 6, 5),
            "end":   datetime.date(2020, 7, 31)
        }

        dateTwo = {
            "start": datetime.date(2020, 7, 5),
            "end":   datetime.date(2020, 8, 22)
        }

        self.assertTrue(SectionMeeting.doesDateConflict(dateOne, dateTwo))

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