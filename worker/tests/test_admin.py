from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from worker.models import Position


class AdminSiteTest(TestCase):
    def setUp(self):
        position = Position.objects.create(name="Electrician")
        self.worker = get_user_model().objects.create_superuser(
            username="admin",
            password="1qazcde3",
            position=position
        )
        self.client.force_login(self.worker)

    def test_admin_site_position_displayed(self):
        url = reverse("admin:worker_worker_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)

    def test_admin_detail_position_displayed(self):
        url = reverse("admin:worker_worker_change", args=[1])
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)

    def test_admin_add_position_displayed(self):
        url = reverse("admin:worker_worker_add")
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)
