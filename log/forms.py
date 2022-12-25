from django import forms
from django.contrib.auth import get_user_model

from log.models import (
    Breakdown,
    BreakdownType,
    Equipment,
    EquipmentType,
)


class EquipmentTypeForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Equipment type name",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = EquipmentType
        fields = ("name",)


class EquipmentForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Equipment name",
                "class": "form-control"
            }
        )
    )
    inventory_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Equipment inventory number",
                "class": "form-control"
            }
        )
    )
    type = forms.ModelChoiceField(
        queryset=EquipmentType.objects.all(),
        empty_label="Equipment type",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Equipment
        fields = ("name", "inventory_number", "type")


class BreakdownTypeForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Breakdown type name",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = BreakdownType
        fields = ("name",)


class BreakdownForm(forms.ModelForm):
    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.select_related("type"),
        empty_label="Equipment",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    breakdown_type = forms.ModelChoiceField(
        queryset=BreakdownType.objects.all(),
        empty_label="Breakdown type",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    repair_staff = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-select",
            }
        ),
    )
    circumstance = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    status = forms.ChoiceField(
        choices=Breakdown.STATUS_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )
    repair_duration = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Equipment repair duration in minutes",
            }
        ),
    )

    class Meta:
        model = Breakdown
        fields = (
            "equipment",
            "breakdown_type",
            "repair_staff",
            "circumstance",
            "status",
            "repair_duration",
        )


class EquipmentTypeSearchForm(forms.Form):
    searched_equipment_type = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by equipment type name",
                "class": "form-control",
            }
        ),
    )


class BreakdownTypeSearchForm(forms.Form):
    searched_breakdown_type = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by breakdown type name",
                "class": "form-control",
            }
        ),
    )


class BreakdownSearchForm(forms.Form):
    searched_breakdown = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by breakdown type or equipment",
                "class": "form-control",
            }
        ),
    )
    searched_complete_status = forms.BooleanField(
        required=False,
        label="Under repair",
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                "onclick": "this.form.submit();",
            }
        ),
    )


class EquipmentSearchForm(forms.Form):
    searched_equipment = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by type, name or inventory number",
                "class": "form-control",
            }
        ),
    )
