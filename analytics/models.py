from django.conf import settings
from django.db import models

from projects.models import Project


class Regex(models.Model):
    regex = models.CharField('正規表現', max_length=100)
    name = models.CharField('正規表現名', max_length=200, null=True, blank=True)
    project = models.ForeignKey(
        Project,
        verbose_name='プロジェクト',
        on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField('順番', default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="作成者",
        on_delete=models.DO_NOTHING,
        null=True,
    )
    created_at = models.DateTimeField('作成日', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Regex'
    
    def __str__(self):
        return f'<Regex: {self.regex}, {self.project}>'


class WeeklyAll(models.Model):
    project = models.ForeignKey(
        Project,
        verbose_name='プロジェクト',
        on_delete=models.CASCADE
    )
    date = models.DateField('日付') 
    users = models.PositiveIntegerField('ユーザー数', default=0)
    session = models.PositiveIntegerField('流入数', default=0)
    conversion = models.PositiveIntegerField('CV数', default=0)
    conversion_rate = models.FloatField('CVR', default=0.0)
    page_view = models.FloatField('PV', default=0)
    page_view_per_session = models.FloatField('PV/流入数', default=0)
    direct = models.PositiveIntegerField('ダイレクト', default=0)
    organic = models.PositiveIntegerField('自然検索', default=0)
    organic_conversion = models.FloatField('自然検索CV数', default=0)
    organic_conversion_rate = models.FloatField('自然検索CVR', default=0.0)
    paid = models.PositiveIntegerField('有料検索', default=0)
    referral = models.PositiveIntegerField('リファラー', default=0)
    display = models.PositiveIntegerField('ディスプレイ', default=0)
    social = models.PositiveIntegerField('SNS', default=0)
    email = models.PositiveIntegerField('メール', default=0)
    others = models.PositiveIntegerField('その他', default=0)
    
    class Meta:
        verbose_name_plural = 'WeeklyAll'
    
    def __str__(self):
        return f'<WeeklyAll: {self.date}, {self.session}>'


class MonthlyAll(models.Model):
    project = models.ForeignKey(
        Project,
        verbose_name='プロジェクト',
        on_delete=models.CASCADE
    )
    date = models.DateField('日付') 
    users = models.PositiveIntegerField('ユーザー数', default=0)
    session = models.PositiveIntegerField('流入数', default=0)
    conversion = models.PositiveIntegerField('CV数', default=0)
    conversion_rate = models.FloatField('CVR', default=0.0)
    page_view = models.FloatField('PV', default=0)
    page_view_per_session = models.FloatField('PV/流入数', default=0)
    direct = models.PositiveIntegerField('ダイレクト', default=0)
    organic = models.PositiveIntegerField('自然検索', default=0)
    organic_conversion = models.FloatField('自然検索CV数', default=0)
    organic_conversion_rate = models.FloatField('自然検索CVR', default=0.0)
    paid = models.PositiveIntegerField('有料検索', default=0)
    referral = models.PositiveIntegerField('リファラー', default=0)
    display = models.PositiveIntegerField('ディスプレイ', default=0)
    social = models.PositiveIntegerField('SNS', default=0)
    email = models.PositiveIntegerField('メール', default=0)
    others = models.PositiveIntegerField('その他', default=0)
    
    class Meta:
        verbose_name_plural = 'MonthlyAll'
    
    def __str__(self):
        return f'<MonthlyAll: {self.date}, {self.session}>'


class WeeklyDir(models.Model):
    project = models.ForeignKey(
        Project,
        verbose_name='プロジェクト',
        on_delete=models.CASCADE
    )
    regex = models.ForeignKey(
        Regex,
        verbose_name='正規表現',
        on_delete=models.CASCADE
    )
    date = models.DateField('日付') 
    users = models.PositiveIntegerField('ユーザー数', default=0)
    session = models.PositiveIntegerField('流入数', default=0)
    conversion = models.FloatField('CV数', default=0)
    conversion_rate = models.FloatField('CVR', default=0.0)
    page_view = models.FloatField('PV', default=0)
    page_view_per_session = models.FloatField('PV/流入数', default=0)

    class Meta:
        verbose_name_plural = 'WeeklyDir'
    
    def __str__(self):
        return f'<WeeklyDir: {self.regex}, {self.date}, {self.session}>'


class MonthlyDir(models.Model):
    project = models.ForeignKey(
        Project,
        verbose_name='プロジェクト',
        on_delete=models.CASCADE
    )
    regex = models.ForeignKey(
        Regex,
        verbose_name='正規表現',
        on_delete=models.CASCADE
    )
    date = models.DateField('日付') 
    users = models.PositiveIntegerField('ユーザー数', default=0) 
    session = models.PositiveIntegerField('流入数', default=0)
    conversion = models.FloatField('CV数', default=0)
    conversion_rate = models.FloatField('CVR', default=0.0)
    page_view = models.FloatField('PV', default=0)
    page_view_per_session = models.FloatField('PV/流入数', default=0)
    
    class Meta:
        verbose_name_plural = 'MonthlyDir'
    
    def __str__(self):
        return f'<MonthlyDir: {self.regex}, {self.date}, {self.session}>'