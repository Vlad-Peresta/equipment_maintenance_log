from django.test import TestCase

from task.models import TaskType, Task


class TestTaskTypeModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        TaskType.objects.create(name="5S")

    def test_task_type_str(self):
        task_type = TaskType.objects.get(id=1)

        self.assertEqual(str(task_type), task_type.name)

    def test_task_type_fields_quantity(self):
        expected_fields = ["id", "name"]
        model_fields = [field.name for field in TaskType._meta.fields]

        self.assertEqual(expected_fields, model_fields)


class TestTaskModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        task_type = TaskType.objects.create(name="5S")
        Task.objects.create(
            name="Add toolbox",
            description="Add toolbox",
            deadline="2023-11-11",
            is_completed=False,
            priority="urgent",
            task_type=task_type,
        )

    def test_task_str(self):
        task = Task.objects.get(id=1)

        self.assertEqual(
            str(task),
            f"{task.name}, is_completed - {task.is_completed}"
        )

    def test_task_fields_quantity(self):
        expected_fields = [
            "id",
            "name",
            "description",
            "deadline",
            "is_completed",
            "priority",
            "task_type",
        ]
        model_fields = [field.name for field in Task._meta.fields]

        self.assertEqual(expected_fields, model_fields)
