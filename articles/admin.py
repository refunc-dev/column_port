from django.contrib import admin
from articles.models import Article, Keyword, Ranking, Analytics

admin.site.register(Article)
admin.site.register(Keyword)
admin.site.register(Ranking)
admin.site.register(Analytics)