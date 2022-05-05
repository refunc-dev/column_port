from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory

from projects.models import Project
from projects.views import project_list, new_project

UserModel = get_user_model()

class ShowProjectListTest(TestCase):
    def test_project_list_returns_200_and_expected_title(self):
        response = self.client.get('/projects/')
        self.assertContains(response, 'プロジェクト一覧', status_code=200)

    def test_project_list_uses_expected_template(self):
        response = self.client.get('/projects/')
        self.assertTemplateUsed(response, 'projects/index.html')

class RenderProjectListTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username='test_user',
            email='test@example.com',
            password='top_secret_pass0001',
        )
        self.project = Project.objects.create(
            name='name1',
            url='aaa.com',
        )

    def test_should_return_project_name(self):
        request = RequestFactory().get('/projects/')
        request.user = self.user
        response = project_list(request)
        self.assertContains(response, self.project.name)

class CreateProjectTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username='test_user',
            email='test@example.com',
            password='top_secret_pass0001',
        )
        self.client.force_login(self.user)

    def test_render_creation_form(self):
        response = self.client.get('/projects/new/')
        self.assertContains(response, "プロジェクト登録", status_code=200)

    def test_create_project(self):
        data = {'name': '名前', 'url': 'example.com'}
        self.client.post('/projects/new/', data)
        project = Project.objects.get(name='名前')
        self.assertEqual('名前', project.name)
        self.assertEqual('example.com', project.url)