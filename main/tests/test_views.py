from django.test import TestCase
from django.urls import reverse

from main.models import Education, Experience, Project


class MainViewTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Lambda Calculus and Haskell",
            description="welcome back to another recreational programming session with mista zozin",
            category="internship",
            started_at="1990-04-01T00:00:00Z",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'href="{reverse("main:show_experience")}"',
        )

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)


class ExperienceViewTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="JavaScript and TypeScript Programmer",
            description="Web, Node.js, Deno, Bun, Workers, Web extension, WASM.",
            category="research",
            started_at="2018-11-11T00:00:00Z",
        )

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'href="{reverse("main:show_main")}"',
        )

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)


class EducationViewTest(TestCase):
    def setUp(self):
        self.education = Education.objects.create(
            institution="Faculty of Computer Science, Universitas Indonesia",
            program="Bachelor of Computer Science",
            field="Information System",
            started_at="2025-08-25T00:00:00Z",
        )

    def test_education_page(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'href="{reverse("main:show_main")}"',
        )

    def test_empty_education_page(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)


class ProjectViewTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Lambda Calculus and Haskell",
            description="welcome back to another recreational programming session with mista zozin",
            link=None,
            created_at="1990-04-01T00:00:00Z",
        )

    def test_project_page(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'data-api-url="{reverse("api:project-list")}"')
        self.assertContains(response, 'src="/static/js/list.js"')
        self.assertContains(
            response,
            f'href="{reverse("main:show_main")}"',
        )
