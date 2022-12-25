from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from worker.models import Position

WORKER_LIST_URL = reverse("worker:worker-list")
WORKER_CREATE_URL = reverse("worker:worker-create")
WORKER_DETAIL_URL = reverse("worker:worker-detail", args=[1])
WORKER_UPDATE_URL = reverse("worker:worker-update", args=[1])
WORKER_DELETE_URL = reverse("worker:worker-delete", args=[1])

WORKER_TEST_CASES = [
    (
        "test_worker_list_login_required",
        WORKER_LIST_URL,
        200
    ),
    (
        "test_worker_create_login_required",
        WORKER_CREATE_URL,
        200
    ),
    (
        "test_worker_detail_login_required",
        WORKER_DETAIL_URL,
        200
    ),
    (
        "test_worker_update_login_required",
        WORKER_UPDATE_URL,
        200
    ),
    (
        "test_worker_delete_login_required",
        WORKER_DELETE_URL,
        200
    ),
]


class PublicWorkerTest(TestCase):
    def test_worker_public_login_required(self):
        for test_name, url, result in WORKER_TEST_CASES:
            with self.subTest(test_name):
                response = self.client.get(url)
                self.assertNotEqual(result, response.status_code)


class PrivateWorkerTest(TestCase):
    def setUp(self):
        position = Position.objects.create(name="position")
        self.worker = get_user_model().objects.create_superuser(
            username="admin",
            password="1qazcde3",
            position=position
        )
        self.client.force_login(self.worker)

    def test_worker_private_login_required(self):
        for test_name, url, result in WORKER_TEST_CASES:
            with self.subTest(test_name):
                response = self.client.get(url)
                self.assertEqual(result, response.status_code)
