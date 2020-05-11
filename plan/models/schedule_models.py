from djongo import models
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

    def to_dict(self):
        result = {
            'name': self.name,
            'section_type': self.section_type,
            'crn': self.crn,
            'meetings': [meeting.to_dict() for meeting in self.meetings]
        }
        return result


class Schedule(models.Model):
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

    def to_dict(self):
        result = {
            'sections': [section.to_dict() for section in self.sections]
        }
        return result
