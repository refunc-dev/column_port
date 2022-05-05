from django.conf import settings
from django.db import models

class Project(models.Model):
    name = models.CharField('プロジェクト名', max_length=128)
    url = models.CharField('プロジェクトURL', max_length=2083)
    created_by = models.ForeignKey(
                    settings.AUTH_USER_MODEL,
                    verbose_name="作成者",
                    on_delete=models.SET_NULL,
                    null=True
                )
    created_at = models.DateField('作成日', auto_now_add=True)

    def __str__(self):
        return str(self.id)