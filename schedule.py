
import datetime
from enum import Enum
import jsonschema

# https://json-schema.org/understanding-json-schema/
"""
Represents a schedule for some sectuib. When initialized, takes in the JSON
representation and converts it into an internal representation
with this class.

The granularity is chosen to be a section, as a course's sections can be used
independently when organizing a term. The course will be composed of sections

Provides utility functions that help evaluate section schedules. Namely:
- Does a section conflict with any other provided sections
- 
"""

class Section():
    SCHEMA =  {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "pattern": "^[ABT]\\d{2}$"
            },
            "type": {
                "type": "string",
                "enum": ["lecture", "lab", "tutorial"]
            },
            "crn": {
                "type": "integer"
            },
            "meetings": {
                "type": "array",
                "items": {
                    "type": "object"
                }
                
            }
        },
        "required": ["name", "type", "crn", "meetings"]
    }

    """ 
    The class is responsible for validating the arguments and storing 
    the internal representation.
    """
    def __init__(self, jsonData):
        jsonschema.validate(jsonData, self.SCHEMA)

        self.name = jsonData["name"]
        self.type = SectionType(jsonData["type"])
        self.crn  = jsonData["crn"]
        self.meetings = [SectionMeeting(jsonElement) for jsonElement in jsonData["meetings"]]

    """
    Takes a Section object, and determines if any of the meetings conflict
    at any point in time.
    """
    ## TESTED: NO
    def doesSectionConflict(self, section):
        assert type(section) == Section

        # For each meeting pair in both sections, check if conflict exists
        for toCompareMeeting in section.meetings:
            for meeting in self.meetings:
                # Both `toCompareMeeting` and `meeting` are of type SectionMeeting
                if meeting.doesMeetingConflict(toCompareMeeting):
                    return True 
        return False

class SectionMeeting():
    SCHEMA = {
        "type": "object",
        "properties": {
            "days": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": ["M","T","W","R","F"]
                }
            },
            "location": {
                "type": "string"
            },
            "date range": {
                "type": "object",
                "properties": {
                    "start": {
                        "type": "string",
                        "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "end": {
                        "type": "string",
                        "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    }
                },
                "required": ["start", "end"]
            },
            "times": {
                "type": "object",
                "properties": {
                    "start": {
                        "type": "string",
                        "pattern": "^\\d{2}:\\d{2}$"
                    },
                    "end": {
                        "type": "string",
                        "pattern": "^\\d{2}:\\d{2}$"
                    }
                },
                "required": ["start", "end"]
            }
        },
        "required": ["days", "location", "date range", "times"]
    }


    def __init__(self, jsonData):
        jsonschema.validate(jsonData, self.SCHEMA)

        # Do some sort of validation here
        self.days = [WeekdayString(day) for day in jsonData["days"]] 
        self.location = jsonData["location"]

        # Parse meeting dates
        startYear, startMonth, startDay = [int(x) for x in jsonData["date range"]["start"].split("-")]
        endYear, endMonth, endDay = [int(x) for x in jsonData["date range"]["end"].split("-")]
        self.dates =  {
            "start": datetime.date(startYear, startMonth, startDay),
            "end": datetime.date(endYear, endMonth, endDay)
        }

        # Parse meeting times
        startHour, startMinute = [int(x) for x in jsonData["times"]["start"].split(":")]
        endHour, endMinute     = [int(x) for x in jsonData["times"]["end"].split(":")]
        self.times = {
            "start": datetime.time(startHour, startMinute),
            "end":   datetime.time(endHour, endMinute)
        }

    """
    Determines if the given meeting conflicts with the current meeting
    at any point in time.
    """
    ## TESTED: NO
    def doesMeetingConflict(self, meeting):
        assert type(meeting) == SectionMeeting
        
        if meeting.dates["end"] < self.dates["start"] \
            or meeting.dates["start"] > self.dates["end"]:
            # Skip if the date ranges don't overlap
            return False

        # If the start and end dates overlap for 6 days or less, then
        # we must only check the specific days they overlap for time 
        # conflicts.

        # First case where overlap is less than 7 days
        if (meeting.dates["end"] - self.dates["start"]) < 7:
            # Only compare the overlapping weekdays where both meetings are offered
            overlappingWeekdays = SectionMeeting.getWeekdaysInDateRange(self.dates["start"], meeting.dates["end"])
            weekdaysToCompare = [day for day in overlappingWeekdays if (day in meeting.days) and (day in self.days)]
            # If any weekdays are to compare, then same time conflict between all those weekdays
            if len(weekdaysToCompare) == 0:
                return False

            if SectionMeeting.doesTimeConflict(self.times, meeting.times):
                return True 

        # Second case where overlap is less than 7 days
        elif (self.dates["end"] - meeting.dates["start"]) < 7:
            overlappingWeekdays = SectionMeeting.getWeekdaysInDateRange(meeting.dates["start"], self.dates["end"])
            weekdaysToCompare = [day for day in overlappingWeekdays if (day in meeting.days) and (day in self.days)]
            if len(weekdaysToCompare) == 0:
                return False

            if SectionMeeting.doesTimeConflict(self.times, meeting.times):
                return True

        # Third case when overlap is 7 days or more. Any weekdays are applicable
        else:
            weekdaysToCompare = [day for day in list(Weekday) if (day in meeting.days) and (day in self.days)]
            if len(weekdaysToCompare) == 0:
                return False

            if SectionMeeting.doesTimeConflict(self.times, meeting.times):
                return True 

        return False

    """
    Takes two datetime.date objects, and returns the list of weekdays spanned by the 2 dates.
    """
    @staticmethod
    def getWeekdaysInDateRange(dateOne, dateTwo):
        assert type(dateOne) == datetime.date 
        assert type(dateTwo) == datetime.date 
        assert dateTwo >= dateOne 

        weekdays = []
        for _ in range(7):
            weekdays.append(Weekday(dateOne.weekday())) 
            if dateOne == dateTwo:
                return weekdays
            dateOne = dateOne + datetime.timedelta(days=1)
        return weekdays

    """
    Takes two variables, each a dictionary with "start" and "end" datetime.time elements
    """
    @staticmethod
    def doesTimeConflict(timeOne, timeTwo):
        # TODO: Validation
        if timeOne["end"] > timeTwo["start"] \
            and timeOne["start"] < timeTwo["end"]:
            return True
        else:
            return False

class SectionType(Enum):
    LECTURE = "lecture"
    LAB = "lab"
    TUTORIAL = "tutorial"

class Weekday(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3 
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class WeekdayString(Enum):
    MONDAY = "M"
    TUESDAY = "T"
    WEDNESDAY = "W"
    THURSDAY = "R" 
    FRIDAY = "F"
    SATURDAY = "S"
    SUNDAY = "Z"   