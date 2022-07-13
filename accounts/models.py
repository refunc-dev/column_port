from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class GetOrNoneManager(UserManager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class User(AbstractUser):
    objects = GetOrNoneManager()