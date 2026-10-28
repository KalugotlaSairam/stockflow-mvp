
from django.contrib import admin
from django.urls import path

from inventory import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.dashboard_view, name="dashboard"),

    path("signup/", views.signup_view, name="signup"),

    path("login/", views.login_view, name="login"),

    path("logout/", views.logout_view, name="logout"),

    path("products/", views.product_list, name="product_list"),

path(
    "products/add/",
    views.product_create,
    name="product_create"
),

path(
    "products/<int:product_id>/edit/",
    views.product_edit,
    name="product_edit"
),

path(
    "products/<int:product_id>/delete/",
    views.product_delete,
    name="product_delete"
),

path("settings/", views.settings_view, name="settings"),
]
