import datetime
from aenum import MultiValueEnum
from enum import Enum
import jsonschema
import schema

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
    SCHEMA = schema.SECTION_SCHEMA

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
    SCHEMA = schema.SECTION_MEETING_SCHEMA

    def __init__(self, jsonData):
        jsonschema.validate(jsonData, self.SCHEMA)

        # Do some sort of validation here
        self.days = [Weekday(day) for day in jsonData["days"]] 
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
    def doesMeetingConflict(self, meeting):
        assert type(meeting) == SectionMeeting 

        if not SectionMeeting.doesDateConflict(self.dates, meeting.dates):
            # Skip if the date ranges don't overlap
            return False

        # If the start and end dates overlap for 6 days or less, then
        # we must only check the specific days they overlap for time 
        # conflicts.
        if abs(meeting.dates["end"] - self.dates["start"]) < datetime.timedelta(days=7) \
            or abs(self.dates["end"] - meeting.dates["start"]) < datetime.timedelta(days=7):
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

        if dateTwo < dateOne:
            earlierTime = dateTwo
            laterTime = dateOne
        else:
            earlierTime = dateOne 
            laterTime = dateTwo 

        weekdays = []
        for _ in range(7):
            weekdays.append(Weekday(earlierTime.weekday())) 
            if earlierTime == laterTime:
                return weekdays
            earlierTime = earlierTime + datetime.timedelta(days=1)
        return weekdays

    """
    Takes two variables and determines if the dates conflict
    """
    @staticmethod 
    def doesDateConflict(dateOne, dateTwo):
        # TODO: Validation
        if dateOne["end"] >= dateTwo["start"] \
            and dateOne["start"] <= dateTwo["end"]:
            return True
        return False

    """
    Takes two variables, each a dictionary with "start" and "end" datetime.time elements
    """
    @staticmethod
    #TODO: Test overlapping over days?
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

class Weekday(MultiValueEnum):
    MONDAY = 0, "M"
    TUESDAY = 1, "T"
    WEDNESDAY = 2, "W"
    THURSDAY = 3, "R"
    FRIDAY = 4, "F"
    SATURDAY = 5, "S"
    SUNDAY = 6, "Z"