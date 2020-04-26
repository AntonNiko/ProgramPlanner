from djongo import models

class CourseCode(models.Model):
    subject = models.CharField(max_length=4)
    number = models.CharField(max_length=8)

class DateRange(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

class TimeRange(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()