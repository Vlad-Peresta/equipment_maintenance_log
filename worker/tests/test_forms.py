from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from worker.models import Position

WORKER_LIST_URL = reverse("worker:worker-list")
WORKER_CREATE_URL = reverse("worker:worker-create")
WORKER_UPDATE_URL = reverse("worker:worker-update", args=[1])
WORKER_LOGIN_URL = reverse("worker:worker-login")


class TestCheckForms(TestCase):
    def setUp(self):
        position = Position.objects.create(name="position")
        self.worker = get_user_model().objects.create_superuser(
            username="admin",
            password="1qazcde3",
            position=position
        )
        self.client.force_login(self.worker)

    def test_worker_search_form_on_site_pages_exist(self):
        response = self.client.get(WORKER_LIST_URL)

        self.assertIn("search_form", response.context)

    def test_worker_create_form_fields(self):
        response = self.client.get(WORKER_CREATE_URL)
        expected_fields = (
            "username",
            "first_name",
            "last_name",
            "position",
            "email",
            "password1",
            "password2",
        )

        for field in expected_fields:
            self.assertIn(field, response.context["form"].fields)

    def test_worker_update_form_fields(self):
        response = self.client.get(WORKER_UPDATE_URL)
        expected_fields = (
            "username",
            "first_name",
            "last_name",
            "position",
            "email",
        )

        for field in expected_fields:
            self.assertIn(field, response.context["form"].fields)

    def test_worker_login_form_fields(self):
        response = self.client.get(WORKER_LOGIN_URL)

        self.assertIn("username", response.context["form"].fields)
        self.assertIn("password", response.context["form"].fields)
