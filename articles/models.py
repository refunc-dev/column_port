from django.conf import settings
from django.db import models

from projects.models import Project


class Keyword(models.Model):
    keyword = models.TextField("キーワード", blank=False, primary_key=True)
    volume = models.PositiveIntegerField('検索数', default=0)
    url_1 = models.CharField('1位', max_length=2083, blank=True, null=True)
    url_2 = models.CharField('2位', max_length=2083, blank=True, null=True)
    url_3 = models.CharField('3位', max_length=2083, blank=True, null=True)
    url_4 = models.CharField('4位', max_length=2083, blank=True, null=True)
    url_5 = models.CharField('5位', max_length=2083, blank=True, null=True)
    url_6 = models.CharField('6位', max_length=2083, blank=True, null=True)
    url_7 = models.CharField('7位', max_length=2083, blank=True, null=True)
    url_8 = models.CharField('8位', max_length=2083, blank=True, null=True)
    url_9 = models.CharField('9位', max_length=2083, blank=True, null=True)
    url_10 = models.CharField('10位', max_length=2083, blank=True, null=True)
    url_11 = models.CharField('11位', max_length=2083, blank=True, null=True)
    url_12 = models.CharField('12位', max_length=2083, blank=True, null=True)
    url_13 = models.CharField('13位', max_length=2083, blank=True, null=True)
    url_14 = models.CharField('14位', max_length=2083, blank=True, null=True)
    url_15 = models.CharField('15位', max_length=2083, blank=True, null=True)
    url_16 = models.CharField('16位', max_length=2083, blank=True, null=True)
    url_17 = models.CharField('17位', max_length=2083, blank=True, null=True)
    url_18 = models.CharField('18位', max_length=2083, blank=True, null=True)
    url_19 = models.CharField('19位', max_length=2083, blank=True, null=True)
    url_20 = models.CharField('20位', max_length=2083, blank=True, null=True)
    url_21 = models.CharField('21位', max_length=2083, blank=True, null=True)
    url_22 = models.CharField('22位', max_length=2083, blank=True, null=True)
    url_23 = models.CharField('23位', max_length=2083, blank=True, null=True)
    url_24 = models.CharField('24位', max_length=2083, blank=True, null=True)
    url_25 = models.CharField('25位', max_length=2083, blank=True, null=True)
    url_26 = models.CharField('26位', max_length=2083, blank=True, null=True)
    url_27 = models.CharField('27位', max_length=2083, blank=True, null=True)
    url_28 = models.CharField('28位', max_length=2083, blank=True, null=True)
    url_29 = models.CharField('29位', max_length=2083, blank=True, null=True)
    url_30 = models.CharField('30位', max_length=2083, blank=True, null=True)
    url_31 = models.CharField('31位', max_length=2083, blank=True, null=True)
    url_32 = models.CharField('32位', max_length=2083, blank=True, null=True)
    url_33 = models.CharField('33位', max_length=2083, blank=True, null=True)
    url_34 = models.CharField('34位', max_length=2083, blank=True, null=True)
    url_35 = models.CharField('35位', max_length=2083, blank=True, null=True)
    url_36 = models.CharField('36位', max_length=2083, blank=True, null=True)
    url_37 = models.CharField('37位', max_length=2083, blank=True, null=True)
    url_38 = models.CharField('38位', max_length=2083, blank=True, null=True)
    url_39 = models.CharField('39位', max_length=2083, blank=True, null=True)
    url_40 = models.CharField('40位', max_length=2083, blank=True, null=True)
    url_41 = models.CharField('41位', max_length=2083, blank=True, null=True)
    url_42 = models.CharField('42位', max_length=2083, blank=True, null=True)
    url_43 = models.CharField('43位', max_length=2083, blank=True, null=True)
    url_44 = models.CharField('44位', max_length=2083, blank=True, null=True)
    url_45 = models.CharField('45位', max_length=2083, blank=True, null=True)
    url_46 = models.CharField('46位', max_length=2083, blank=True, null=True)
    url_47 = models.CharField('47位', max_length=2083, blank=True, null=True)
    url_48 = models.CharField('48位', max_length=2083, blank=True, null=True)
    url_49 = models.CharField('49位', max_length=2083, blank=True, null=True)
    url_50 = models.CharField('50位', max_length=2083, blank=True, null=True)
    url_51 = models.CharField('51位', max_length=2083, blank=True, null=True)
    url_52 = models.CharField('52位', max_length=2083, blank=True, null=True)
    url_53 = models.CharField('53位', max_length=2083, blank=True, null=True)
    url_54 = models.CharField('54位', max_length=2083, blank=True, null=True)
    url_55 = models.CharField('55位', max_length=2083, blank=True, null=True)
    url_56 = models.CharField('56位', max_length=2083, blank=True, null=True)
    url_57 = models.CharField('57位', max_length=2083, blank=True, null=True)
    url_58 = models.CharField('58位', max_length=2083, blank=True, null=True)
    url_59 = models.CharField('59位', max_length=2083, blank=True, null=True)
    url_60 = models.CharField('60位', max_length=2083, blank=True, null=True)
    url_61 = models.CharField('61位', max_length=2083, blank=True, null=True)
    url_62 = models.CharField('62位', max_length=2083, blank=True, null=True)
    url_63 = models.CharField('63位', max_length=2083, blank=True, null=True)
    url_64 = models.CharField('64位', max_length=2083, blank=True, null=True)
    url_65 = models.CharField('65位', max_length=2083, blank=True, null=True)
    url_66 = models.CharField('66位', max_length=2083, blank=True, null=True)
    url_67 = models.CharField('67位', max_length=2083, blank=True, null=True)
    url_68 = models.CharField('68位', max_length=2083, blank=True, null=True)
    url_69 = models.CharField('69位', max_length=2083, blank=True, null=True)
    url_70 = models.CharField('70位', max_length=2083, blank=True, null=True)
    url_71 = models.CharField('71位', max_length=2083, blank=True, null=True)
    url_72 = models.CharField('72位', max_length=2083, blank=True, null=True)
    url_73 = models.CharField('73位', max_length=2083, blank=True, null=True)
    url_74 = models.CharField('74位', max_length=2083, blank=True, null=True)
    url_75 = models.CharField('75位', max_length=2083, blank=True, null=True)
    url_76 = models.CharField('76位', max_length=2083, blank=True, null=True)
    url_77 = models.CharField('77位', max_length=2083, blank=True, null=True)
    url_78 = models.CharField('78位', max_length=2083, blank=True, null=True)
    url_79 = models.CharField('79位', max_length=2083, blank=True, null=True)
    url_80 = models.CharField('80位', max_length=2083, blank=True, null=True)
    url_81 = models.CharField('81位', max_length=2083, blank=True, null=True)
    url_82 = models.CharField('82位', max_length=2083, blank=True, null=True)
    url_83 = models.CharField('83位', max_length=2083, blank=True, null=True)
    url_84 = models.CharField('84位', max_length=2083, blank=True, null=True)
    url_85 = models.CharField('85位', max_length=2083, blank=True, null=True)
    url_86 = models.CharField('86位', max_length=2083, blank=True, null=True)
    url_87 = models.CharField('87位', max_length=2083, blank=True, null=True)
    url_88 = models.CharField('88位', max_length=2083, blank=True, null=True)
    url_89 = models.CharField('89位', max_length=2083, blank=True, null=True)
    url_90 = models.CharField('90位', max_length=2083, blank=True, null=True)
    url_91 = models.CharField('91位', max_length=2083, blank=True, null=True)
    url_92 = models.CharField('92位', max_length=2083, blank=True, null=True)
    url_93 = models.CharField('93位', max_length=2083, blank=True, null=True)
    url_94 = models.CharField('94位', max_length=2083, blank=True, null=True)
    url_95 = models.CharField('95位', max_length=2083, blank=True, null=True)
    url_96 = models.CharField('96位', max_length=2083, blank=True, null=True)
    url_97 = models.CharField('97位', max_length=2083, blank=True, null=True)
    url_98 = models.CharField('98位', max_length=2083, blank=True, null=True)
    url_99 = models.CharField('99位', max_length=2083, blank=True, null=True)
    url_100 = models.CharField('100位', max_length=2083, blank=True, null=True)
    registered_at = models.DateField('登録日', auto_now_add=True)
    updated_at = models.DateField('更新日', blank=True, null=True)
 
    def __str__(self):
        return f'<Keyword: {self.keyword}>'


class Article(models.Model):
    project_id = models.ForeignKey(
        Project,
        verbose_name="プロジェクト",
        on_delete=models.CASCADE
    )
    url = models.CharField('記事URL', max_length=2083)
    title = models.CharField('タイトル', max_length=100)
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
    keywords = models.ManyToManyField(Keyword, blank=True)
    created_at = models.DateField('作成日', auto_now_add=True)
 
    def __str__(self):
        return f'<Article: {self.url}, {self.project_id}>'


class Ranking(models.Model):
    rw_choices = (
        ('right', '○'),
        ('wrong', '×')
    )

    article_id = models.ForeignKey(
        Article,
        verbose_name="記事",
        on_delete=models.CASCADE
    )
    keyword_id = models.ForeignKey(
        Keyword,
        verbose_name="キーワード",
        on_delete=models.CASCADE
    )
    ranking = models.PositiveIntegerField('順位', default=0)
    ranking_page = models.CharField('ランクインページ', max_length=2083, null=True)
    date = models.DateField('日付') 
    right_wrong = models.CharField('正誤表', max_length=5, choices=rw_choices, blank=True)

    def __str__(self):
        return f'<Ranking: {self.article_id.url}, {self.keyword_id.keyword}, {self.ranking}>'


class Analytics(models.Model):
    path = models.CharField('記事URL', max_length=2083)
    date = models.DateField('日付') 
    session = models.PositiveIntegerField('流入数', default=0)
    conversion = models.FloatField('CV数', default=0)
    conversion_rate = models.FloatField('CVR', default=0.0)
    article_id = models.ForeignKey(
        Article,
        verbose_name='記事',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Analytics'

    def __str__(self):
        return str(self.session)