from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Course)
admin.site.register(CourseOffering)
admin.site.register(Section)
admin.site.register(Meeting)

admin.site.register(Schedule)
admin.site.register(ScheduleSection)

admin.site.register(Sequence)
admin.site.register(Term)
admin.site.register(TermCourse)
