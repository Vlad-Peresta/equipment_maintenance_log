from django.contrib.auth import get_user_model
from django.test import TestCase

from worker.models import Position


class TestPositionModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Position.objects.create(name="Electrician")

    def test_position_str(self):
        position = Position.objects.get(id=1)

        self.assertEqual(str(position), position.name)

    def test_position_fields_quantity(self):
        expected_fields = ["id", "name"]
        model_fields = [field.name for field in Position._meta.fields]

        self.assertEqual(expected_fields, model_fields)


class TestWorkerModel(TestCase):
    def setUp(self):
        position = Position.objects.create(name="position")
        self.worker = get_user_model().objects.create_superuser(
            username="admin",
            password="1qazcde3",
            position=position
        )
        self.client.force_login(self.worker)

    def test_worker_str(self):
        self.assertEqual(
            str(self.worker),
            f"{self.worker.first_name} {self.worker.last_name} "
            f"({self.worker.username})"
        )

    def test_worker_fields_quantity(self):
        expected_fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "position",
            "email",
        ]
        model_fields = [
            field.name
            for field in get_user_model()._meta.fields
        ]

        for field in expected_fields:
            self.assertIn(field, model_fields)
