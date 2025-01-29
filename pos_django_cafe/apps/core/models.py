import json
from typing import Any, Optional

from django.db import models


class OrderStatus(models.Model):
    name = models.CharField("Status code", max_length=50, unique=True)
    description = models.CharField("Description", max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.description or ''


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    table_number = models.PositiveIntegerField("Table number")
    items = models.JSONField("Items list", default=list)
    total_price = models.DecimalField(
        "Total price",
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    status = models.ForeignKey(
        OrderStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Order status",
    )

    class Meta:
        ordering = ['id']

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.total_price = sum(item['price'] for item in self.items)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Order {self.id} for table {self.table_number} ({self.status})"
