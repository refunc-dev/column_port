from rest_framework import generics, mixins, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from projects.models import Keyword
from ranking.models import KeywordSerp, Ranking
from api.serializers import KeywordListSerializer, KeywordUpdateSerializer, KeywordSerpSerializer

from urllib.parse import urlparse
import datetime
import re


class KeywordListAPIView(generics.ListAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordListSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return Keyword.objects.filter(updated_at__lt=datetime.date.today(), lock_flag=False).values('id','keyword','updated_at')


class KeywordUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordUpdateSerializer


class KeywordSerpCreateAPIView(generics.CreateAPIView):
    queryset = KeywordSerp.objects.all()
    serializer_class = KeywordSerpSerializer

    def perform_create(self, serializer):
        serps = serializer.save()
        keyword = serps.keyword
        websites = keyword.website_set.all()
        for website in websites:
            is_ranked = False
            for i in range(1, 101):
                url = getattr(serps, f'url_{i}')
                title = getattr(serps, f'title_{i}')
                if url and re.search(website.domain, url):
                    Ranking.objects.create(
                        website=website,
                        keyword=keyword,
                        ranking=int(i),
                        ranking_page=urlparse(url).path,
                        title_link=title,
                        date=datetime.date.today(),
                    )
                    is_ranked = True
                    break
            if not is_ranked:
                Ranking.objects.create(
                    website=website,
                    keyword=keyword,
                    ranking=0,
                    ranking_page=None,
                    title_link=None,
                    date=datetime.date.today(),
                )