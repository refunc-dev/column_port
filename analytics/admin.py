from django.contrib import admin
from analytics.models import Regex, WeeklyAll, WeeklyDir, MonthlyAll, MonthlyDir

admin.site.register(Regex)
admin.site.register(WeeklyAll)
admin.site.register(WeeklyDir)
admin.site.register(MonthlyAll)
admin.site.register(MonthlyDir)