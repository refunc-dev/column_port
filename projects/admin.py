from django.contrib import admin
from projects.models import Project, Regex, Weekly, Monthly

admin.site.register(Project)
admin.site.register(Regex)
admin.site.register(Weekly)
admin.site.register(Monthly)