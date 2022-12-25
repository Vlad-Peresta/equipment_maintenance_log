from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task.models import TaskType, Task
from worker.models import Position

TASK_LIST_URL = reverse("task:task-list")
TASK_CREATE_URL = reverse("task:task-create")
TASK_DETAIL_URL = reverse("task:task-detail", args=[1])
TASK_UPDATE_URL = reverse("task:task-update", args=[1])
TASK_DELETE_URL = reverse("task:task-delete", args=[1])
TOGGLE_ASSIGN_TASK_URL = reverse("task:toggle-assign-task", args=[1])
TOGGLE_PERFORM_TASK_URL = reverse("task:toggle-perform-task", args=[1])

TASK_TYPE_LIST_URL = reverse("task:task-type-list")
TASK_TYPE_CREATE_URL = reverse("task:task-type-create")
TASK_TYPE_UPDATE_URL = reverse("task:task-type-update", args=[1])
TASK_TYPE_DELETE_URL = reverse("task:task-type-delete", args=[1])

TASK_TYPE_TEST_CASES = [
    (
        "test_task_type_list_login_required",
        TASK_TYPE_LIST_URL,
        200
    ),
    (
        "test_task_type_create_login_required",
        TASK_TYPE_CREATE_URL,
        200
    ),
    (
        "test_task_type_update_login_required",
        TASK_TYPE_UPDATE_URL,
        200
    ),
    (
        "test_task_type_delete_login_required",
        TASK_TYPE_DELETE_URL,
        200
    ),
]


class PublicTaskTest(TestCase):
    def test_task_public_login_required(self):
        test_cases = [
            (
                "test_task_list_login_required",
                TASK_LIST_URL,
                200
            ),
            (
                "test_task_detail_login_required",
                TASK_DETAIL_URL,
                200,
            ),
            (
                "test_task_update_login_required",
                TASK_UPDATE_URL,
                200
            ),
            (
                "test_task_create_login_required",
                TASK_CREATE_URL,
                200
            ),
            (
                "test_task_delete_login_required",
                TASK_DELETE_URL,
                200,
            ),
            (
                "test_task_toggle_assign_login_required",
                TOGGLE_ASSIGN_TASK_URL,
                200
            ),
            (
                "test_task_toggle_perform_login_required",
                TOGGLE_PERFORM_TASK_URL,
                200
            )
        ]

        for test_name, url, result in test_cases:
            with self.subTest(test_name):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, result)


class PrivateTaskTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        position = Position.objects.create(name="position")
        get_user_model().objects.create_superuser(
            username="admin",
            password="1qazcde3",
            position=position
        )

        task_type = TaskType.objects.create(name="5S")
        Task.objects.create(
            name="Add toolbox",
            description="Add toolbox",
            deadline="2023-11-11",
            is_completed=False,
            priority="urgent",
            task_type=task_type,
        )

    def test_task_private_login_required(self):
        test_cases = [
            (
                "test_task_list_login_required",
                TASK_LIST_URL,
                200
            ),
            (
                "test_task_detail_login_required",
                TASK_DETAIL_URL,
                200,
            ),
            (
                "test_task_update_login_required",
                TASK_UPDATE_URL,
                200
            ),
            (
                "test_task_create_login_required",
                TASK_CREATE_URL,
                200
            ),
            (
                "test_task_delete_login_required",
                TASK_DELETE_URL,
                200,
            ),
            (
                "test_task_toggle_assign_login_required",
                TOGGLE_ASSIGN_TASK_URL,
                302
            ),
            (
                "test_task_toggle_perform_login_required",
                TOGGLE_PERFORM_TASK_URL,
                302
            )
        ]

        self.client.force_login(get_user_model().objects.get(id=1))

        for test_name, url, result in test_cases:
            with self.subTest(test_name):
                response = self.client.get(url)
                self.assertEqual(response.status_code, result)


class PublicTaskTypeTest(TestCase):
    def test_task_type_public_login_required(self):
        for test_name, url, result in TASK_TYPE_TEST_CASES:
            with self.subTest(test_name):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, result)


class PrivateTaskTypeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        position = Position.objects.create(name="position")
        get_user_model().objects.create_superuser(
            username="admin",
            password="1qazcde3",
            position=position
        )

        TaskType.objects.create(name="5S")

    def test_task_type_private_login_required(self):
        self.client.force_login(get_user_model().objects.get(id=1))

        for test_name, url, result in TASK_TYPE_TEST_CASES:
            with self.subTest(test_name):
                response = self.client.get(url)
                self.assertEqual(response.status_code, result)
