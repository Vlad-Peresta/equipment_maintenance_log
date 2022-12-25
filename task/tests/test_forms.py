from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from worker.models import Position

TASK_LIST_URL = reverse("task:task-list")
TASK_CREATE_URL = reverse("task:task-create")
TASK_TYPE_LIST_URL = reverse("task:task-type-list")
TASK_TYPES_CREATE_URL = reverse("task:task-type-create")


class TestCheckForms(TestCase):
    @classmethod
    def setUpTestData(cls):
        position = Position.objects.create(name="position")
        get_user_model().objects.create_superuser(
            username="admin",
            password="1qazcde3",
            position=position
        )

    def test_form_on_site_pages_exist(self):
        test_cases = [
            (
                "test_task_search_form",
                TASK_LIST_URL,
                "search_form"
            ),
            (
                "test_task_type_search_form",
                TASK_TYPE_LIST_URL,
                "search_form"
            ),
            (
                "test_task_type_create_update_form",
                TASK_TYPES_CREATE_URL,
                "form"
            )
        ]

        self.client.force_login(
            get_user_model().objects.get(id=1)
        )

        for test_name, url, context_name in test_cases:
            with self.subTest(test_name):
                response = self.client.get(url)

                self.assertTrue(context_name in response.context)

    def test_task_search_form_fields(self):
        self.client.force_login(
            get_user_model().objects.get(id=1)
        )
        response = self.client.get(TASK_LIST_URL)

        self.assertIn("searched_task", response.context["search_form"].fields)
        self.assertIn(
            "searched_complete_status", response.context["search_form"].fields
        )

    def test_task_create_update_form_fields(self):
        self.client.force_login(
            get_user_model().objects.get(id=1)
        )
        response = self.client.get(TASK_CREATE_URL)

        self.assertIn("task_type", response.context["form"].fields)
        self.assertIn("name", response.context["form"].fields)
        self.assertIn("priority", response.context["form"].fields)
        self.assertIn("deadline", response.context["form"].fields)
        self.assertIn("description", response.context["form"].fields)
        self.assertIn("assignees", response.context["form"].fields)
