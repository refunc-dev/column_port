from django.contrib import admin
from projects.models import Project, Regex, WeeklyAll, WeeklyDir, MonthlyAll, MonthlyDir

admin.site.register(Project)
admin.site.register(Regex)
admin.site.register(WeeklyAll)
admin.site.register(WeeklyDir)
admin.site.register(MonthlyAll)
admin.site.register(MonthlyDir)