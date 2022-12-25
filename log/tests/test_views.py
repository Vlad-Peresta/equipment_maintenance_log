from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from log.models import EquipmentType, Equipment, BreakdownType, Breakdown
from worker.models import Position

BREAKDOWN_TYPE_CREATE_URL = reverse("log:breakdown-type-create")
BREAKDOWN_CREATE_URL = reverse("log:log-create")
BREAKDOWN_TYPE_LIST_URL = reverse("log:breakdown-type-list")
BREAKDOWN_LIST_URL = reverse("log:log-list")
EQUIPMENT_TYPE_CREATE_URL = reverse("log:equipment-type-create")
EQUIPMENT_CREATE_URL = reverse("log:equipment-create")
EQUIPMENT_LIST_URL = reverse("log:equipment-list")
EQUIPMENT_TYPE_UPDATE_URL = reverse("log:equipment-type-update", args=[1])
EQUIPMENT_TYPE_LIST_URL = reverse("log:equipment-type-list")
EQUIPMENT_TYPE_DELETE_URL = reverse("log:equipment-type-delete", args=[1])
EQUIPMENT_DELETE_URL = reverse("log:equipment-delete", args=[1])
EQUIPMENT_UPDATE_URL = reverse("log:equipment-update", args=[1])
BREAKDOWN_TYPE_DELETE_URL = reverse("log:breakdown-type-delete", args=[1])
BREAKDOWN_TYPE_UPDATE_URL = reverse("log:breakdown-type-update", args=[1])
BREAKDOWN_DELETE_URL = reverse("log:log-delete", args=[1])
BREAKDOWN_UPDATE_URL = reverse("log:log-update", args=[1])
BREAKDOWN_DETAIL_URL = reverse("log:log-detail", args=[1])
INDEX = reverse("log:index")
TOGGLE_PERFORM_REPAIR = reverse("log:toggle-perform-repair", args=[1])

LOG_TEST_CASES = [
    (
        "test_equipment_type_list_login_required",
        EQUIPMENT_TYPE_LIST_URL,
        200
    ),
    (
        "test_equipment_type_create_login_required",
        EQUIPMENT_TYPE_CREATE_URL,
        200
    ),
    (
        "test_equipment_type_update_login_required",
        EQUIPMENT_TYPE_UPDATE_URL,
        200
    ),
    (
        "test_equipment_type_delete_login_required",
        EQUIPMENT_TYPE_DELETE_URL,
        200
    ),
    (
        "test_equipment_list_login_required",
        EQUIPMENT_LIST_URL,
        200
    ),
    (
        "test_equipment_create_login_required",
        EQUIPMENT_CREATE_URL,
        200
    ),
    (
        "test_equipment_update_login_required",
        EQUIPMENT_UPDATE_URL,
        200
    ),
    (
        "test_equipment_delete_login_required",
        EQUIPMENT_DELETE_URL,
        200
    ),
    (
        "test_breakdown_type_list_login_required",
        BREAKDOWN_TYPE_LIST_URL,
        200
    ),
    (
        "test_breakdown_type_create_login_required",
        BREAKDOWN_TYPE_CREATE_URL,
        200
    ),
    (
        "test_breakdown_type_update_login_required",
        BREAKDOWN_TYPE_UPDATE_URL,
        200
    ),
    (
        "test_breakdown_type_delete_login_required",
        BREAKDOWN_TYPE_DELETE_URL,
        200
    ),
    (
        "test_breakdown_list_login_required",
        BREAKDOWN_LIST_URL,
        200
    ),
    (
        "test_breakdown_detail_login_required",
        BREAKDOWN_DETAIL_URL,
        200
    ),
    (
        "test_breakdown_create_login_required",
        BREAKDOWN_CREATE_URL,
        200
    ),
    (
        "test_breakdown_update_login_required",
        BREAKDOWN_UPDATE_URL,
        200
    ),
    (
        "test_breakdown_delete_login_required",
        BREAKDOWN_DELETE_URL,
        200
    ),
    (
        "test_index_login_required",
        INDEX,
        200
    ),
]


class PublicTest(TestCase):
    def test_public_login_required(self):
        for test_name, url, result in LOG_TEST_CASES:
            with self.subTest(test_name):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, result)


class PrivateTest(TestCase):
    def setUp(self) -> None:
        equipment_type = EquipmentType.objects.create(name="IMM")
        equipment = Equipment.objects.create(
            name="R1C1",
            inventory_number="ABS123456",
            type=equipment_type
        )
        breakdown_type = BreakdownType.objects.create(
            name="Motor failure"
        )
        Breakdown.objects.create(
            equipment=equipment,
            breakdown_type=breakdown_type,
            circumstance="Some reason",
        )
        position = Position.objects.create(name="position")
        self.worker = get_user_model().objects.create_superuser(
            username="admin",
            password="1qazcde3",
            position=position
        )
        self.client.force_login(self.worker)

    def test_private_login_required(self):
        for test_name, url, result in LOG_TEST_CASES:
            with self.subTest(test_name):
                response = self.client.get(url)
                self.assertEqual(response.status_code, result)
