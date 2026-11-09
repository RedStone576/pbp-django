from django.test import TestCase

from main.models import Education, Experience, Project


class ExperienceModelTest(TestCase):
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


class EducationModelTest(TestCase):
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


class ProjectModelTest(TestCase):
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
