from django.conf import settings
from django.db import models

from projects.models import Project


class Article(models.Model):
    url = models.CharField('記事URL', max_length=2083)
    title = models.CharField('title', max_length=100)
    published_at = models.DateField('公開日')
    updated_at = models.DateField('更新日')
    person_in_charge = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="担当",
        on_delete=models.SET_NULL,
        null=True,
        related_name="articles_in_charge"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="作成者",
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_articles'
    )
    created_at = models.DateField('作成日', auto_now_add=True)
    project_id = models.ForeignKey(
        Project,
        verbose_name="プロジェクト",
        on_delete=models.CASCADE
    )
 
    def __str__(self):
        return str(self.id)


class Keyword(models.Model):
    keyword = models.TextField("キーワード", blank=False)
    volume = models.PositiveIntegerField('検索数', default=0)
    article_id = models.ForeignKey(
        Article,
        verbose_name="記事",
        on_delete=models.CASCADE
    )
 
    def __str__(self):
        return self.keyword


class Ranking(models.Model):
    rw_choices = (
        ('right', '○'),
        ('wrong', '×')
    )

    ranking = models.PositiveIntegerField('順位', default=0)
    ranking_page = models.CharField('ランクインページ', max_length=2083, null=True)
    date = models.DateField('日付') 
    right_wrong = models.CharField('正誤表', max_length=5, choices=rw_choices, blank=True)
    keyword_id = models.ForeignKey(
        Keyword,
        verbose_name="キーワード",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.ranking)


class Analytics(models.Model):
    path = models.CharField('記事URL', max_length=2083)
    year_week = models.PositiveIntegerField('週', default=0) 
    session = models.PositiveIntegerField('流入数', default=0)
    conversion_rate = models.FloatField('CVR', default=0.0)
    conversion = models.FloatField('CV数', default=0)
    article_id = models.ForeignKey(
        Article,
        verbose_name='記事',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Analytics'

    def __str__(self):
        return str(self.session)