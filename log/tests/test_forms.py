from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from log.models import (
    Breakdown,
    BreakdownType,
    Equipment,
    EquipmentType,
)
from worker.models import Position


BREAKDOWN_TYPE_CREATE_URL = reverse("log:breakdown-type-create")
BREAKDOWN_CREATE_URL = reverse("log:log-create")
BREAKDOWN_TYPE_LIST_URL = reverse("log:breakdown-type-list")
BREAKDOWN_LIST_URL = reverse("log:log-list")
EQUIPMENT_TYPE_CREATE_URL = reverse("log:equipment-type-create")
EQUIPMENT_CREATE_URL = reverse("log:equipment-create")
EQUIPMENT_LIST_URL = reverse("log:equipment-list")
EQUIPMENT_TYPE_LIST_URL = reverse("log:equipment-type-list")


class TestCheckForms(TestCase):
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

    def test_form_on_site_pages_exist(self):
        test_cases = [
            (
                "test_equipment_search_form",
                EQUIPMENT_LIST_URL,
                "search_form"
            ),
            (
                "test_equipment_type_search_form",
                EQUIPMENT_TYPE_LIST_URL,
                "search_form"
            ),
            (
                "test_equipment_type_form",
                EQUIPMENT_TYPE_CREATE_URL,
                "form"
            ),
            (
                "test_breakdown_type_search_form",
                BREAKDOWN_TYPE_LIST_URL,
                "search_form"
            ),
            (
                "test_breakdown_type_form",
                BREAKDOWN_TYPE_CREATE_URL,
                "form"
            ),

        ]

        for test_name, url, context_name in test_cases:
            with self.subTest(test_name):
                response = self.client.get(url)
                print(response.context)

                self.assertTrue(context_name in response.context)

    def test_breakdown_search_form_fields(self):
        response = self.client.get(BREAKDOWN_LIST_URL)

        self.assertIn(
            "searched_breakdown",
            response.context["search_form"].fields
        )
        self.assertIn(
            "searched_complete_status",
            response.context["search_form"].fields
        )

    def test_equipment_create_update_form_fields(self):
        response = self.client.get(EQUIPMENT_CREATE_URL)
        expected_fields = ["name", "inventory_number", "type"]

        for field in expected_fields:
            self.assertIn(field, response.context["form"].fields)

    def test_breakdown_create_update_form_fields(self):
        response = self.client.get(BREAKDOWN_CREATE_URL)
        expected_fields = [
            "equipment",
            "breakdown_type",
            "repair_staff",
            "circumstance",
            "status",
            "repair_duration"
        ]

        for field in expected_fields:
            self.assertIn(field, response.context["form"].fields)
