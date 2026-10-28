
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages

from .forms import SignupForm, LoginForm
from .models import Organization, UserProfile

from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError

from .models import Product
from .forms import ProductForm

from django.db import models

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = SignupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            organization_name = form.cleaned_data["organization_name"]

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )

            organization = Organization.objects.create(
                name=organization_name
            )

            UserProfile.objects.create(
                user=user,
                organization=organization
            )

        login(request, user)
        messages.success(
            request,
            f"Welcome to StockFlow, {organization.name}!"
        )

        return redirect("dashboard")

    return render(
        request,
        "signup.html",
        {"form": form}
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["username"].strip().lower()

        user = User.objects.get(email__iexact=email)

        login(request, user)

        return redirect("dashboard")

    return render(
        request,
        "login.html",
        {"form": form}
    )


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")

    return redirect("dashboard")


@login_required
def dashboard_view(request):
    # Temporary placeholder.
    # We will add real inventory calculations later.
    return render(request, "dashboard.html")


@login_required
def product_list(request):
    organization = request.user.profile.organization

    products = Product.objects.filter(
        organization=organization
    ).order_by("-created_at")

    search_query = request.GET.get("q", "").strip()

    if search_query:
        products = products.filter(
            models.Q(name__icontains=search_query)
            | models.Q(sku__icontains=search_query)
        )

    return render(
        request,
        "products.html",
        {
            "products": products,
            "search_query": search_query,
        }
    )

@login_required
def product_create(request):
    organization = request.user.profile.organization

    form = ProductForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        product.organization = organization

        try:
            with transaction.atomic():
                product.save()
        except IntegrityError:
            form.add_error(
                "sku",
                "This SKU already exists in your organization."
            )
        else:
            messages.success(
                request,
                "Product added successfully."
            )
            return redirect("product_list")

    return render(
        request,
        "product_form.html",
        {
            "form": form,
            "page_title": "Add Product",
        }
    )

@login_required
def product_edit(request, product_id):
    organization = request.user.profile.organization

    product = get_object_or_404(
        Product,
        id=product_id,
        organization=organization
    )

    form = ProductForm(
        request.POST or None,
        instance=product
    )

    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                form.save()
        except IntegrityError:
            form.add_error(
                "sku",
                "This SKU already exists in your organization."
            )
        else:
            messages.success(
                request,
                "Product updated successfully."
            )
            return redirect("product_list")

    return render(
        request,
        "product_form.html",
        {
            "form": form,
            "page_title": "Edit Product",
        }
    )

@login_required
def product_delete(request, product_id):
    organization = request.user.profile.organization

    product = get_object_or_404(
        Product,
        id=product_id,
        organization=organization
    )

    if request.method == "POST":
        product.delete()

        messages.success(
            request,
            "Product deleted successfully."
        )

    return redirect("product_list")

@login_required
def dashboard_view(request):
    organization = request.user.profile.organization

    products = Product.objects.filter(
        organization=organization
    ).order_by("-updated_at")

    total_products = products.count()

    total_quantity = sum(
        products.values_list("quantity", flat=True)
    )

    low_stock_items = [
        product for product in products
        if product.is_low_stock
    ]

    return render(
        request,
        "dashboard.html",
        {
            "organization": organization,
            "total_products": total_products,
            "total_quantity": total_quantity,
            "low_stock_count": len(low_stock_items),
            "low_stock_items": low_stock_items[:10],
        }
    )

@login_required
def settings_view(request):
    organization = request.user.profile.organization

    if request.method == "POST":
        threshold = request.POST.get(
            "default_low_stock_threshold", ""
        ).strip()

        if not threshold.isdigit():
            messages.error(
                request,
                "Enter a valid non-negative integer."
            )

        elif int(threshold) > 1000000:
            messages.error(
                request,
                "The threshold is too large."
            )

        else:
            organization.default_low_stock_threshold = int(threshold)
            organization.save(
                update_fields=["default_low_stock_threshold"]
            )

            messages.success(
                request,
                "Default low-stock threshold updated."
            )

            return redirect("settings")

    return render(
        request,
        "settings.html",
        {"organization": organization}
    )