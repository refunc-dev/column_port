from django.core.management.base import BaseCommand, CommandError
from projects.models import Keyword

from projects.management.commands.utils.generate_keywords_api import generate_keywords_api

class Command(BaseCommand):

    def handle(self, *args, **options):
        keywords = Keyword.objects.all()
        for k in keywords:
            volume = generate_keywords_api(k.keyword)
            k.volume = volume
            k.save()