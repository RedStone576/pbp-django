from types import SimpleNamespace

from django.contrib.auth.models import User
from django.test import TestCase

from main.api.serializers import ProjectSerializer
from main.models import Project


class ProjectSerializerTest(TestCase):
    def test_validates_and_cleans_project_text(self):
        serializer = ProjectSerializer(data={
            "title": " <b>Website</b> ",
            "description": "<p>A <em>portfolio</em></p>",
        })

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["title"], "Website")
        self.assertEqual(serializer.validated_data["description"], "A portfolio")

    def test_rejects_blank_and_tag_only_titles(self):
        for title in ("   ", "<b></b>"):
            serializer = ProjectSerializer(data={
                "title": title,
                "description": "Description",
            })
            self.assertFalse(serializer.is_valid())
            self.assertIn("title", serializer.errors)

    def test_star_fields_are_output_only_and_reflect_request_user(self):
        project = Project.objects.create(title="Website", description="Portfolio")
        user = User.objects.create_user(username="visitor", password="password")
        serializer = ProjectSerializer(project, context={
            "request": SimpleNamespace(user=user),
        })
        self.assertEqual(serializer.data["star_count"], 0)
        self.assertFalse(serializer.data["is_starred"])

        project.starred_by.add(user)
        serializer = ProjectSerializer(project, context={
            "request": SimpleNamespace(user=user),
        })
        self.assertEqual(serializer.data["star_count"], 1)
        self.assertTrue(serializer.data["is_starred"])
        self.assertEqual(serializer.data["starred_by_names"], "visitor")

        input_serializer = ProjectSerializer(data={
            "title": "Another",
            "description": "Description",
            "star_count": 99,
            "is_starred": True,
            "starred_by_names": "forged",
        })
        self.assertTrue(input_serializer.is_valid(), input_serializer.errors)
        self.assertNotIn("star_count", input_serializer.validated_data)
