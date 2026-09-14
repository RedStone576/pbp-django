from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Education, Project

# i just copied all this from `python manage.py dumpdata`
class MainTest(TestCase):
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
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(
            response,
            f'href="{reverse("main:show_experience")}"',
        )

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)


class ExperienceTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="JavaScript and TypeScript Programmer",
            description="Web, Node.js, Deno, Bun, Workers, Web extension, WASM.",
            category="research",
            started_at="2018-11-11T00:00:00Z",
        )

    def test_experience_model(self):
        self.assertEqual(
            str(self.experience),
            "JavaScript and TypeScript Programmer",
        )
        self.assertEqual(
            self.experience.description,
            "Web, Node.js, Deno, Bun, Workers, Web extension, WASM.",
        )
        self.assertEqual(
            self.experience.category,
            "research",
        )
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(
            response,
            "JavaScript and TypeScript Programmer",
        )
        self.assertContains(
            response,
            "Web, Node.js, Deno, Bun, Workers, Web extension, WASM.",
        )
        self.assertContains(response, "Research")
        self.assertContains(response, "Sekarang")
        self.assertContains(
            response,
            f'href="{reverse("main:show_main")}"',
        )

    def test_empty_experience_page(self):
        Experience.objects.all().delete()

        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(
            response,
            "Belum ada pengalaman yang ditambahkan.",
        )

    def test_completed_experience(self):
        self.experience.ended_at = "2026-09-14T00:00:00Z"
        self.experience.save()

        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertNotContains(response, "Sekarang")
        self.assertContains(response, "September 2026")


class EducationTest(TestCase):
    def setUp(self):
        self.education = Education.objects.create(
            institution="Faculty of Computer Science, Universitas Indonesia",
            program="Bachelor of Computer Science",
            field="Information System",
            started_at="2025-08-25T00:00:00Z",
        )

    def test_education_model(self):
        self.assertEqual(
            str(self.education),
            "Bachelor of Computer Science",
        )
        self.assertEqual(
            self.education.institution,
            "Faculty of Computer Science, Universitas Indonesia",
        )
        self.assertEqual(
            self.education.program,
            "Bachelor of Computer Science",
        )
        self.assertEqual(
            self.education.field,
            "Information System",
        )

    def test_education_page(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")
        self.assertContains(
            response,
            "Faculty of Computer Science, Universitas Indonesia",
        )
        self.assertContains(
            response,
            "Bachelor of Computer Science",
        )
        self.assertContains(
            response,
            "Information System",
        )
        self.assertContains(
            response,
            f'href="{reverse("main:show_main")}"',
        )

    def test_empty_education_page(self):
        Education.objects.all().delete()

        response = self.client.get(reverse("main:show_education"))

        self.assertContains(
            response,
            "Belum ada pendidikan yang ditambahkan.",
        )


class ProjectTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Lambda Calculus and Haskell",
            description="welcome back to another recreational programming session with mista zozin",
            link=None,
            created_at="1990-04-01T00:00:00Z",
        )

    def test_project_model(self):
        self.assertEqual(
            str(self.project),
            "Lambda Calculus and Haskell",
        )
        self.assertEqual(
            self.project.description,
            "welcome back to another recreational programming session with mista zozin",
        )
        self.assertIsNone(self.project.link)

    def test_project_page(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(
            response,
            "Lambda Calculus and Haskell",
        )
        self.assertContains(
            response,
            "welcome back to another recreational programming session with mista zozin",
        )
        self.assertContains(
            response,
            f'href="{reverse("main:show_main")}"',
        )

    def test_empty_project_page(self):
        Project.objects.all().delete()

        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(
            response,
            "Belum ada proyek yang ditambahkan.",
        )
