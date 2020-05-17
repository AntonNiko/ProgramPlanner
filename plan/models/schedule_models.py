import datetime
from django.contrib.auth.models import User
from djongo import models
from plan.utils import DateUtils, Weekday
from .utils_models import DateRange, TimeRange


class MeetingDay(models.Model):
    day = models.CharField(
        max_length=2,
        choices=[
            ('M', 'monday'),
            ('T', 'tuesday'),
            ('W', 'wednesday'),
            ('R', 'thursday'),
            ('F', 'friday'),
            ('S', 'saturday'),
            ('Z', 'sunday')
        ]
    )

    def to_dict(self):
        result = {
            'day': self.day
        }
        return result


class Meeting(models.Model):
    days = models.ArrayField(
        model_container=MeetingDay
    )
    location = models.CharField(max_length=30)
    date_range = models.EmbeddedField(
        model_container=DateRange
    )
    time_range = models.EmbeddedField(
        model_container=TimeRange
    )

    def does_meeting_conflict(self, meeting_to_compare):

        if not DateUtils.do_dates_overlap(self.date_range, meeting_to_compare.date_range):
            # Skip if the date ranges don't overlap
            return False

        # If the start and end dates overlap for 6 days or less, then
        # we must only check the specific days they overlap for time
        # conflicts.
        if abs(meeting_to_compare.date_range.end_date - self.date_range.start_date) < datetime.timedelta(days=7) \
            or abs(self.date_range.end_date - meeting_to_compare.date_range.start_date) < datetime.timedelta(days=7):

            overlapping_weekdays = DateUtils.get_weekdays_in_date_range(meeting_to_compare.date_range.start_date, self.date_range.end_date)
            # TODO: Double-check compatibility  with MeetingDay ArrayField
            weekdays_to_compare = [day for day in overlapping_weekdays if (day in meeting_to_compare.days) and (day in self.days)]

            if len(weekdays_to_compare) == 0:
                return False
            if DateUtils.do_times_overlap(self.time_range, meeting_to_compare.time_range):
                return True

        # Third case when overlap is 7 days or more. Any weekdays are applicable
        else:
            weekdays_to_compare = [day for day in list(Weekday) if (day in meeting_to_compare.days) and (day in self.days)]
            if len(weekdays_to_compare) == 0:
                return False

            # TODO: Double-check compatibility with MeetingDay
            if DateUtils.do_times_overlap(self.time_range, meeting_to_compare.time_range):
                return True

        return False

    def to_dict(self):
        result = {
            'days': [day.to_dict()['day'] for day in self.days],
            'location': self.location,
            'date_range': self.date_range,
            'time_range': self.time_range
        }
        return result


class Section(models.Model):
    name = models.CharField(max_length=4)
    section_type = models.CharField(
        max_length=20,
        choices=[
            ('lecture', 'lecture'),
            ('lab', 'lab'),
            ('tutorial', 'tutorial')
        ]
    )
    crn = models.IntegerField()
    meetings = models.ArrayField(
        model_container=Meeting
    )

    def does_section_conflict(self, section_to_compare):
        for meeting_to_compare in section_to_compare:
            for meeting in self.meetings:
                if meeting.does_meeting_conflict(meeting_to_compare):
                    return True

        return False

    def to_dict(self):
        result = {
            'name': self.name,
            'section_type': self.section_type,
            'crn': self.crn,
            'meetings': [meeting.to_dict() for meeting in self.meetings]
        }
        return result


class Schedule(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    term_type = models.PositiveSmallIntegerField(
        choices=[
            (1, 'spring'),
            (2, 'summer'),
            (3, 'fall')
        ]
    )
    name = models.CharField(max_length=100)
    sections = models.ArrayReferenceField(
        to=Section,
        on_delete=models.CASCADE,
        blank=False
    )

    def does_section_conflict(self, section_to_compare):
        result = {'conflicts': False, 'data': []}
        for section in self.sections.all():
            conflict_exists = section.does_section_conflict(section_to_compare)
            if conflict_exists:
                result['conflicts'] = True
                result['data'].append(section.crn)

        return result

    def to_dict(self):
        result = {
            'year': self.year,
            'term_type': self.term_type,
            'name': self.name,
            'sections': [section.to_dict() for section in self.sections.all()]
        }
        return result
