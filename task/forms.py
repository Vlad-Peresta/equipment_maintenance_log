from django import forms
from django.contrib.auth import get_user_model

from task.models import TaskType, Task


class TaskTypeForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Task type name", "class": "form-control"}
        )
    )

    class Meta:
        model = TaskType
        fields = ("name",)


class TaskForm(forms.ModelForm):
    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        empty_label="Task type",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Task name", "class": "form-control"}
        )
    )
    priority = forms.ChoiceField(
        choices=Task.PRIORITY_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )
    deadline = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "placeholder": "Deadline"
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-select",
            }
        ),
    )

    class Meta:
        model = Task
        fields = (
            "task_type",
            "name",
            "priority",
            "deadline",
            "description",
            "assignees",
        )


class TaskSearchForm(forms.Form):
    searched_task = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by task type or name",
                "class": "form-control",
            }
        ),
    )
    searched_complete_status = forms.BooleanField(
        required=False,
        label="Tasks in process",
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                "onclick": "this.form.submit();",
            }
        ),
    )


class TaskTypeSearchForm(forms.Form):
    searched_task_type = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by task type name",
                "class": "form-control"
            }
        ),
    )
