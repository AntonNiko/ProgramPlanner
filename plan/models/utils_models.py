from djongo import models

class CourseCode(models.Model):
    subject = models.CharField(max_length=4)
    number = models.CharField(max_length=8)

    def to_dict(self):
        result = {
            'subject': self.subject,
            'number': self.number
        }
        return result


class DateRange(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def to_dict(self):
        result = {
            'start_date': self.start_date,
            'end_date': self.end_date
        }
        return result


class TimeRange(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def to_dict(self):
        result = {
            'start_time': self.start_time,
            'end_time': self.end_time
        }
        return 