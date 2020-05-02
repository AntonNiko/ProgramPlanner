from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from djongo import models
from .utils_models import DateRange, TimeRange

class MeetingDay(models.Model):
    day = models.CharField(
        max_length = 2,
        choices = [
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
        model_container = MeetingDay
    )
    location = models.CharField(max_length=30)
    date_range = models.EmbeddedField(
        model_container = DateRange
    )
    time_range = models.EmbeddedField(
        model_container = TimeRange
    )

    def to_dict(self):
        result = {
            'days': [day.to_dict() for day in self.days],
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
        model_container = Meeting
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
    sections = models.ArrayField(
        model_container = Section
    )

    def to_dict(self):
        result = {
            'sections': [section.to_dict() for section in self.sections]
        }
        return result
