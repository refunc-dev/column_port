from django.contrib import admin
from articles.models import Article, ArticleAnalytics

admin.site.register(Article)
admin.site.register(ArticleAnalytics)