from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from worker.models import Position


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "First name", "class": "form-control"}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Last name", "class": "form-control"}
        )
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        empty_label="Choose position",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "class": "form-control"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password check", "class": "form-control"}
        )
    )

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "position",
            "email",
            "password1",
            "password2",
        )


class WorkerUpdateForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "First name", "class": "form-control"}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Last name", "class": "form-control"}
        )
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        empty_label="Choose position",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "class": "form-control"}
        )
    )

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "position",
            "email",
        )


class WorkerSearchForm(forms.Form):
    searched_worker = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by first name, last name or username",
            }
        ),
    )
