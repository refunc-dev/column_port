import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone

from colorfield.fields import ColorField


class GetOrNoneManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class Keyword(models.Model):
    keyword = models.CharField("キーワード", max_length=1000)
    volume = models.PositiveIntegerField('検索数', default=0)
    registered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="登録者",
        on_delete=models.CASCADE
    )
    registered_at = models.DateTimeField('登録日', auto_now_add=True)
    updated_at = models.DateField('更新日', blank=True, null=True)
    objects = GetOrNoneManager()

    def __str__(self):
        return f'<Keyword: {self.keyword}>'


class Website(models.Model):
    domain = models.CharField('ドメイン名', primary_key=True, max_length=2083)
    keywords = models.ManyToManyField(
        Keyword,
        verbose_name="キーワード",
        through="WebsiteKeywordRelation",
        through_fields=("website", "keyword"),
        blank=True
    )
    registered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="登録者",
        on_delete=models.CASCADE
    )
    registered_at = models.DateField('登録日', auto_now_add=True)
    objects = GetOrNoneManager()
    
    def __str__(self):
        return f'<Website: {self.domain}>'


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('プロジェクト名', max_length=256)
    website = models.ForeignKey(
        Website,
        verbose_name='サイト',
        on_delete=models.CASCADE,
        related_name="website_projects"
    )
    color = ColorField(default='#144A6E')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="作成者",
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_projects"
    )
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="メンバー",
        blank=True,
        related_name='members_projects'
    )
    competitors = models.ManyToManyField(
        Website,
        verbose_name="競合サイト",
        through="ProjectCompetitorRelation",
        through_fields=("project", "competitor"),
        blank=True,
        related_name="competitors_projects"
    )
    objects = GetOrNoneManager()

    def __str__(self):
        return f'<Project: {self.name}, {self.website.domain}>'


class WebsiteKeywordRelation(models.Model):
    website = models.ForeignKey(
        Website,
        verbose_name='サイト',
        on_delete=models.CASCADE
    )
    keyword = models.ForeignKey(
        Keyword,
        verbose_name='キーワード',
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        Project,
        verbose_name='プロジェクト',
        on_delete=models.CASCADE,
        null=True
    )
    registered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="登録者",
        on_delete=models.CASCADE
    )
    registered_at = models.DateTimeField('登録日', auto_now_add=True)
    objects = GetOrNoneManager()

    def __str__(self):
        return f'<{self.website.domain}, {self.keyword.keyword}>'

class ProjectCompetitorRelation(models.Model):
    project = models.ForeignKey(
        Project,
        verbose_name='プロジェクト',
        on_delete=models.CASCADE
    ) 
    competitor = models.ForeignKey(
        Website,
        verbose_name='競合サイト',
        on_delete=models.CASCADE
    )
    color = ColorField(default='#D96738')
    registered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="登録者",
        on_delete=models.CASCADE
    )
    registered_at = models.DateTimeField('登録日', auto_now_add=True)
    objects = GetOrNoneManager()

    def __str__(self):
        return f'<{self.project.name}, {self.competitor.domain}, {self.color}>'