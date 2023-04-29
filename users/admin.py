from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from users.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "gender",
            "age",
            "introduction",
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "name",
            "gender",
            "age",
            "introduction",
            "is_active",
            "is_admin",
        ]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["email", "name", "gender", "age", "introduction", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Information", {"fields": ["name", "gender", "age", "introduction"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "name",
                    "gender",
                    "age",
                    "introduction",
                    "password1",
                    "password2",
                ],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)

admin.site.unregister(Group)
