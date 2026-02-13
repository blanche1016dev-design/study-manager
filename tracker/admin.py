from django.contrib import admin

from .models import Goal, LearningLog

admin.site.register(LearningLog)
admin.site.register(Goal)
