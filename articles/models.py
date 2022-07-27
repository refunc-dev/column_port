import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone

from projects.models import Keyword, Website, Project


class GetOrNoneManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        verbose_name="プロジェクト",
        on_delete=models.CASCADE
    )
    path = models.CharField('記事パス', max_length=2083)
    title = models.CharField('タイトル', max_length=100)
    published_at = models.DateField('公開日')
    updated_at = models.DateTimeField('更新日', default=timezone.now, null=True)
    person_in_charge = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="担当",
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles_in_charge'
    )
    category = models.CharField('カテゴリ', max_length=100, null=True)
    keywords = models.ManyToManyField(
        Keyword,
        verbose_name="キーワード",
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="作成者",
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_articles'
    )
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    objects = GetOrNoneManager()

 
    def __str__(self):
        return f'<Article: {self.project.name} | {self.path}>'


class ArticleAnalytics(models.Model):
    article = models.ForeignKey(
        Article,
        verbose_name='記事',
        on_delete=models.CASCADE
    )
    date = models.DateField('日付') 
    session = models.PositiveIntegerField('流入数', default=0)
    conversion = models.FloatField('CV数', default=0)
    conversion_rate = models.FloatField('CVR', default=0.0)
    objects = GetOrNoneManager()

    class Meta:
        verbose_name_plural = 'ArticleAnalytics'

    def __str__(self):
        return f'<Analytics: {self.article.path} | {self.date} | {self.session}>'