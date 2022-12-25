from django.test import TestCase

from log.models import (
    Breakdown,
    BreakdownType,
    Equipment,
    EquipmentType,
)


class TestEquipmentTypeModel(TestCase):
    def setUp(self) -> None:
        self.equipment_type = EquipmentType.objects.create(name="IMM")

    def test_equipment_type_str(self):
        self.assertEqual(str(self.equipment_type), self.equipment_type.name)

    def test_equipment_type_fields_quantity(self):
        expected_fields = ["id", "name"]
        model_fields = [field.name for field in EquipmentType._meta.fields]

        self.assertEqual(expected_fields, model_fields)


class TestEquipmentModel(TestCase):
    def setUp(self) -> None:
        self.equipment_type = EquipmentType.objects.create(name="IMM")
        self.equipment = Equipment.objects.create(
            name="R1C1",
            inventory_number="ABS123456",
            type=self.equipment_type
        )

    def test_equipment_str(self):
        self.assertEqual(
            str(self.equipment),
            f"{self.equipment.name} - {self.equipment_type}"
        )

    def test_equipment_fields_quantity(self):
        expected_fields = ["id", "name", "inventory_number", "type"]
        model_fields = [field.name for field in Equipment._meta.fields]

        self.assertEqual(expected_fields, model_fields)


class TestBreakdownTypeModel(TestCase):
    def setUp(self) -> None:
        self.breakdown_type = BreakdownType.objects.create(
            name="Motor failure"
        )

    def test_breakdown_type_str(self):
        self.assertEqual(str(self.breakdown_type), self.breakdown_type.name)

    def test_breakdown_type_fields_quantity(self):
        expected_fields = ["id", "name"]
        model_fields = [field.name for field in BreakdownType._meta.fields]

        self.assertEqual(expected_fields, model_fields)


class TestBreakdownModel(TestCase):
    def setUp(self) -> None:
        equipment_type = EquipmentType.objects.create(name="IMM")
        self.equipment = Equipment.objects.create(
            name="R1C1",
            inventory_number="ABS123456",
            type=equipment_type
        )
        self.breakdown_type = BreakdownType.objects.create(
            name="Motor failure"
        )
        self.breakdown = Breakdown.objects.create(
            equipment=self.equipment,
            breakdown_type=self.breakdown_type,
            circumstance="Some reason",
        )

    def test_breakdown_str(self):
        self.assertEqual(
            str(self.breakdown),
            f"{self.equipment} - {self.breakdown.time}"
        )

    def test_breakdown_fields_quantity(self):
        expected_fields = [
            "id",
            "equipment",
            "breakdown_type",
            "circumstance",
            "time",
            "status",
            "repair_duration"
        ]
        model_fields = [field.name for field in Breakdown._meta.fields]

        self.assertEqual(expected_fields, model_fields)
