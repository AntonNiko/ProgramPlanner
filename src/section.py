import datetime
from enum import Enum
import jsonschema
import schema
from utils import DateRange, TimeRange, DateUtils, Weekday

class Section():
    """ 
    The class is responsible for validating the arguments and storing 
    the internal representation.
    """
    SCHEMA = schema.SECTION_SCHEMA

    def __init__(self, jsonData):
        jsonschema.validate(jsonData, self.SCHEMA)

        self.name = jsonData["name"]
        self.type = SectionType(jsonData["type"])
        self.crn  = jsonData["crn"]
        self.meetings = [Meeting(jsonElement) for jsonElement in jsonData["meetings"]]

    def doesSectionConflict(self, section):
        """
        Takes a Section object, and determines if any of the meetings conflict
        at any point in time.
        """
        assert type(section) == Section

        # For each meeting pair in both sections, check if conflict exists
        for toCompareMeeting in section.meetings:
            for meeting in self.meetings:
                # Both `toCompareMeeting` and `meeting` are of type SectionMeeting
                if meeting.doesMeetingConflict(toCompareMeeting):
                    return True 
        return False


class SectionType(Enum):
    LECTURE = "lecture"
    LAB = "lab"
    TUTORIAL = "tutorial"


class Meeting():
    SCHEMA = schema.SECTION_MEETING_SCHEMA

    def __init__(self, jsonData):
        jsonschema.validate(jsonData, self.SCHEMA)

        self.days = [Weekday(day) for day in jsonData["days"]] 
        self.location = jsonData["location"]
        self.dateRange = DateRange(jsonData)
        self.timeRange = TimeRange(jsonData)

    def doesMeetingConflict(self, meeting):
        """
        Determines if the given meeting conflicts with the current meeting
        at any point in time.
        """
        assert type(meeting) == Meeting 

        if not DateUtils.doDatesOverlap(self.dateRange, meeting.dateRange):
            # Skip if the date ranges don't overlap
            return False

        # If the start and end dates overlap for 6 days or less, then
        # we must only check the specific days they overlap for time 
        # conflicts.
        if abs(meeting.dateRange.endDate - self.dateRange.startDate) < datetime.timedelta(days=7) \
            or abs(self.dateRange.endDate - meeting.dateRange.startDate) < datetime.timedelta(days=7):
            overlappingWeekdays = DateUtils.getWeekdaysInDateRange(meeting.dateRange.startDate, self.dateRange.endDate)
            weekdaysToCompare = [day for day in overlappingWeekdays if (day in meeting.days) and (day in self.days)]

            if len(weekdaysToCompare) == 0:
                return False 
            if DateUtils.doTimesOverlap(self.timeRange, meeting.timeRange):
                return True

        # Third case when overlap is 7 days or more. Any weekdays are applicable
        else:
            weekdaysToCompare = [day for day in list(Weekday) if (day in meeting.days) and (day in self.days)]
            if len(weekdaysToCompare) == 0:
                return False

            if DateUtils.doTimesOverlap(self.timeRange, meeting.timeRange):
                return True 

        return False