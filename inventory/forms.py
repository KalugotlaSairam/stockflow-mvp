from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import Organization


class SignupForm(forms.Form):
    organization_name = forms.CharField(
        max_length=150,
        label="Organization Name",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "My Test Store"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "you@example.com"
        })
    )

    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Minimum 8 characters"
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm your password"
        })
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error(
                "confirm_password",
                "Passwords do not match."
            )

        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "you@example.com",
            "autofocus": True
        })
    )

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password"
        })
    )

from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

        fields = [
            "name",
            "sku",
            "description",
            "quantity",
            "cost_price",
            "selling_price",
            "low_stock_threshold",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Product name",
            }),
            "sku": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. SKU-1001",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Optional product description",
            }),
            "quantity": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
            }),
            "cost_price": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
                "step": "0.01",
            }),
            "selling_price": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
                "step": "0.01",
            }),
            "low_stock_threshold": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
                "placeholder": "Leave empty to use organization default",
            }),
        }

    def clean_sku(self):
        return self.cleaned_data["sku"].strip()

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_cost_price(self):
        value = self.cleaned_data.get("cost_price")

        if value is not None and value < 0:
            raise forms.ValidationError(
                "Cost price cannot be negative."
            )

        return value

    def clean_selling_price(self):
        value = self.cleaned_data.get("selling_price")

        if value is not None and value < 0:
            raise forms.ValidationError(
                "Selling price cannot be negative."
            )

        return value