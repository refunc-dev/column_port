from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from projects.models import Project
from projects.forms import ProjectForm
from articles.models import Article, Keyword, Ranking
from articles.forms import ArticleForm


@login_required
def top(request):
    return redirect(project_list)


@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/index.html', {'projects': projects})


@login_required
def project_new(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return redirect(project_list)
    else:
        form = ProjectForm()
    return render(request, 'projects/new.html', {'form': form})


@login_required
def project_detail(request, project_id):
    contents = []
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect(project_detail, project_id=project_id)
    else:
        articles = Article.objects.filter(project_id=project_id).all()
        for article in articles:
            keywords = Keyword.objects.filter(article_id=article.id).all()
            size = len(keywords)
            if size == 0:
                size = 1
            contents.append({'article': article, 'keywords': keywords, 'size': size})
        form = ArticleForm()
        context = {
            'articles': contents,
            'form': form
        }
    return render(request, 'projects/detail.html', context)