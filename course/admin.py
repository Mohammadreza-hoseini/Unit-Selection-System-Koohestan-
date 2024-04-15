from django.contrib import admin
from .models import Subject, Course, ScoreTable

# Register your models here.
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(ScoreTable)
