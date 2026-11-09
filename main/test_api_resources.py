from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework.test import APITestCase

from main.models import Education, Experience


class SharedResourceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser("owner", "owner@example.com", "password")
        self.visitor = User.objects.create_user("visitor", password="password")
        self.editor_group, _ = Group.objects.get_or_create(name="Editor")
      
        self.resources = (
            (Education, "education", {
                "institution": "Example University", "program": "Computer Science", "field": "Systems",
            }, "Computer", "institution", ("institution", "program", "field")),
      
            (Experience, "experience", {
                "title": "Example Role", "description": "Built a useful system", "category": "research",
            }, "Example", "title", ("title", "description")),
        )

    def test_education_and_experience_use_shared_crud_and_star_views(self):
        for model, resource, payload, query, _, _ in self.resources:
            with self.subTest(resource=resource):
                list_url = reverse(f"api:{resource}-list")
      
                self.client.force_authenticate(self.owner)
      
                created = self.client.post(list_url, payload, format="json")
      
                self.assertEqual(created.status_code, 201)
      
                item_id = created.data["id"]
      
                self.assertEqual(model.objects.count(), 1)
                self.assertEqual(len(self.client.get(list_url, {"title": query}).data), 1)
                self.assertNotIn("fields", self.client.get(list_url).data[0])

                detail_url = reverse(f"api:{resource}-detail", args=[item_id])
      
                self.assertEqual(self.client.patch(detail_url, {next(iter(payload)): "Updated"}, format="json").status_code, 200)
                self.client.force_authenticate(user=None)
                self.assertEqual(self.client.post(reverse(f"api:{resource}-star", args=[item_id])).status_code, 403)

                self.client.force_authenticate(self.visitor)
      
                starred = self.client.post(reverse(f"api:{resource}-star", args=[item_id]))
      
                self.assertEqual(starred.status_code, 200)
                self.assertTrue(starred.data["is_starred"])
                self.assertEqual(self.client.delete(detail_url).status_code, 403)

                self.client.force_authenticate(self.owner)
                self.assertEqual(self.client.delete(detail_url).status_code, 204)
                self.assertFalse(model.objects.exists())

    def test_regular_users_and_editors_follow_write_permissions(self):
        for model, resource, payload, _, editable_field, _ in self.resources:
            with self.subTest(resource=resource):
                item = model.objects.create(**payload)
                list_url = reverse(f"api:{resource}-list")
                detail_url = reverse(f"api:{resource}-detail", args=[item.pk])

                self.visitor.groups.clear()
                self.client.force_authenticate(user=None)
                self.assertEqual(self.client.post(list_url, payload, format="json").status_code, 403)
                self.assertEqual(self.client.patch(detail_url, {editable_field: "Unauthorized"}, format="json").status_code, 403)
                self.assertEqual(self.client.delete(detail_url).status_code, 403)
                item.refresh_from_db()
                self.assertEqual(model.objects.count(), 1)
                self.assertEqual(getattr(item, editable_field), payload[editable_field])

                self.client.force_authenticate(self.visitor)
                self.assertEqual(self.client.post(list_url, payload, format="json").status_code, 403)
                self.assertEqual(self.client.patch(detail_url, {editable_field: "Unauthorized"}, format="json").status_code, 403)
                self.assertEqual(self.client.delete(detail_url).status_code, 403)
                item.refresh_from_db()
                self.assertEqual(model.objects.count(), 1)
                self.assertEqual(getattr(item, editable_field), payload[editable_field])

                self.visitor.groups.add(self.editor_group)
                self.assertEqual(self.client.patch(detail_url, {editable_field: "Editor update"}, format="json").status_code, 200)
                self.assertEqual(self.client.post(list_url, payload, format="json").status_code, 403)
                self.assertEqual(self.client.delete(detail_url).status_code, 403)
                item.refresh_from_db()
                self.assertEqual(model.objects.count(), 1)
                self.assertEqual(getattr(item, editable_field), "Editor update")

    def test_text_validation_rejects_tag_only_values_without_creating_records(self):
        self.client.force_authenticate(self.owner)
        for model, resource, payload, _, _, text_fields in self.resources:
            with self.subTest(resource=resource):
                list_url = reverse(f"api:{resource}-list")
                for field in text_fields:
                    with self.subTest(field=field):
                        response = self.client.post(
                            list_url, {**payload, field: "<b> </b>"}, format="json",
                        )
                        self.assertEqual(response.status_code, 400)
                        self.assertIn(field, response.data)
                        self.assertFalse(model.objects.exists())
