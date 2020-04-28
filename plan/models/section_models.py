from django.contrib.auth.models import User
from djongo import models
from .utils_models import DateRange, TimeRange

class MeetingDay(models.Model):
    day = models.CharField(
        max_length = 2,
        choices = [
            ('M', 'Monday'),
            ('T', 'Tuesday'),
            ('W', 'Wednesday'),
            ('R', 'Thursday'),
            ('F', 'Friday'),
            ('S', 'Saturday'),
            ('Z', 'Sunday')
        ]
    ) 

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

class Section(models.Model):
    name = models.CharField(max_length=4)
    section_type = models.CharField(
        max_length=20,
        choices=[
            ('lecture', 'Lecture'),
            ('lab', 'Lab'),
            ('tutorial', 'Tutorial')
        ]
    )
    crn = models.IntegerField()
    meetings = models.ArrayField(
        model_container = Meeting
    )

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    sections = models.ArrayField(
        model_container = Section
    )
