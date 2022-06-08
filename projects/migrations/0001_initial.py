# Generated by Django 4.0.3 on 2022-06-08 02:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='プロジェクト名')),
                ('url', models.CharField(max_length=2083, verbose_name='プロジェクトURL')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='作成日')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='作成者')),
            ],
        ),
        migrations.CreateModel(
            name='Regex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regex', models.CharField(max_length=100, verbose_name='正規表現')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='プロジェクト')),
            ],
            options={
                'verbose_name_plural': 'Regex',
            },
        ),
        migrations.CreateModel(
            name='WeeklyDir',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日付')),
                ('users', models.PositiveIntegerField(default=0, verbose_name='ユーザー数')),
                ('session', models.PositiveIntegerField(default=0, verbose_name='流入数')),
                ('conversion', models.FloatField(default=0, verbose_name='CV数')),
                ('conversion_rate', models.FloatField(default=0.0, verbose_name='CVR')),
                ('page_view', models.FloatField(default=0, verbose_name='PV')),
                ('page_view_per_session', models.FloatField(default=0, verbose_name='PV/流入数')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='プロジェクト')),
                ('regex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.regex', verbose_name='正規表現')),
            ],
            options={
                'verbose_name_plural': 'WeeklyDir',
            },
        ),
        migrations.CreateModel(
            name='WeeklyAll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日付')),
                ('users', models.PositiveIntegerField(default=0, verbose_name='ユーザー数')),
                ('session', models.PositiveIntegerField(default=0, verbose_name='流入数')),
                ('conversion', models.PositiveIntegerField(default=0, verbose_name='CV数')),
                ('conversion_rate', models.FloatField(default=0.0, verbose_name='CVR')),
                ('page_view', models.FloatField(default=0, verbose_name='PV')),
                ('page_view_per_session', models.FloatField(default=0, verbose_name='PV/流入数')),
                ('direct', models.PositiveIntegerField(default=0, verbose_name='ダイレクト')),
                ('organic', models.PositiveIntegerField(default=0, verbose_name='自然検索')),
                ('organic_conversion', models.FloatField(default=0, verbose_name='自然検索CV数')),
                ('organic_conversion_rate', models.FloatField(default=0.0, verbose_name='自然検索CVR')),
                ('paid', models.PositiveIntegerField(default=0, verbose_name='有料検索')),
                ('referral', models.PositiveIntegerField(default=0, verbose_name='リファラー')),
                ('display', models.PositiveIntegerField(default=0, verbose_name='ディスプレイ')),
                ('social', models.PositiveIntegerField(default=0, verbose_name='SNS')),
                ('email', models.PositiveIntegerField(default=0, verbose_name='メール')),
                ('others', models.PositiveIntegerField(default=0, verbose_name='その他')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='プロジェクト')),
            ],
            options={
                'verbose_name_plural': 'WeeklyAll',
            },
        ),
        migrations.CreateModel(
            name='MonthlyDir',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日付')),
                ('users', models.PositiveIntegerField(default=0, verbose_name='ユーザー数')),
                ('session', models.PositiveIntegerField(default=0, verbose_name='流入数')),
                ('conversion', models.FloatField(default=0, verbose_name='CV数')),
                ('conversion_rate', models.FloatField(default=0.0, verbose_name='CVR')),
                ('page_view', models.FloatField(default=0, verbose_name='PV')),
                ('page_view_per_session', models.FloatField(default=0, verbose_name='PV/流入数')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='プロジェクト')),
                ('regex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.regex', verbose_name='正規表現')),
            ],
            options={
                'verbose_name_plural': 'MonthlyDir',
            },
        ),
        migrations.CreateModel(
            name='MonthlyAll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日付')),
                ('users', models.PositiveIntegerField(default=0, verbose_name='ユーザー数')),
                ('session', models.PositiveIntegerField(default=0, verbose_name='流入数')),
                ('conversion', models.PositiveIntegerField(default=0, verbose_name='CV数')),
                ('conversion_rate', models.FloatField(default=0.0, verbose_name='CVR')),
                ('page_view', models.FloatField(default=0, verbose_name='PV')),
                ('page_view_per_session', models.FloatField(default=0, verbose_name='PV/流入数')),
                ('direct', models.PositiveIntegerField(default=0, verbose_name='ダイレクト')),
                ('organic', models.PositiveIntegerField(default=0, verbose_name='自然検索')),
                ('organic_conversion', models.FloatField(default=0, verbose_name='自然検索CV数')),
                ('organic_conversion_rate', models.FloatField(default=0.0, verbose_name='自然検索CVR')),
                ('paid', models.PositiveIntegerField(default=0, verbose_name='有料検索')),
                ('referral', models.PositiveIntegerField(default=0, verbose_name='リファラー')),
                ('display', models.PositiveIntegerField(default=0, verbose_name='ディスプレイ')),
                ('social', models.PositiveIntegerField(default=0, verbose_name='SNS')),
                ('email', models.PositiveIntegerField(default=0, verbose_name='メール')),
                ('others', models.PositiveIntegerField(default=0, verbose_name='その他')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='プロジェクト')),
            ],
            options={
                'verbose_name_plural': 'MonthlyAll',
            },
        ),
    ]
