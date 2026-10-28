
from django.db import models
from django.conf import settings


class Organization(models.Model):
    name = models.CharField(max_length=150)

    default_low_stock_threshold = models.PositiveIntegerField(
        default=5
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=150)

    sku = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    quantity = models.PositiveIntegerField(default=0)

    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    low_stock_threshold = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "sku"],
                name="unique_sku_per_organization"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def effective_low_stock_threshold(self):
        if self.low_stock_threshold is not None:
            return self.low_stock_threshold

        return self.organization.default_low_stock_threshold

    @property
    def is_low_stock(self):
        return (
            self.quantity
            <= self.effective_low_stock_threshold
        )


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="members"
    )

    def __str__(self):
        return f"{self.user.username} - {self.organization.name}"