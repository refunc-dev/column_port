from django.contrib import admin
from projects.models import Keyword, Website, Project, WebsiteKeywordRelation, ProjectCompetitorRelation

admin.site.register(Keyword)
admin.site.register(Website)
admin.site.register(Project)
admin.site.register(WebsiteKeywordRelation)
admin.site.register(ProjectCompetitorRelation)