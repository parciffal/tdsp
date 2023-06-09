from django.db import models
from django.contrib import admin

from .category_model import Category


class BidRequest(models.Model):
    external_id = models.CharField(max_length=255, default=None, null=True, unique=True)
    imp = models.TextField(default=None, null=True)
    click = models.FloatField(default=None, null=True)
    conv = models.FloatField(default=None, null=True)
    site = models.TextField(default=None, null=True)
    ssp_id = models.CharField(max_length=255, default=None, null=True)
    user_id = models.CharField(max_length=255, default=None, null=True)
    categories = models.ManyToManyField(Category)

    class Meta:
        verbose_name_plural = "BidRequest"

    def __str__(self) -> str:
        return str(self.external_id)

    def as_json(self) -> dict:
        data = {
            "id": self.id,
            "external_id": self.external_id,
            "imp": self.imp,
            "click": self.click,
            "conv": self.conv,
            "site": self.site,
            "ssp_id": self.ssp_id,
            "user_id": self.user_id,
            "categories": self.categories,
        }
        return data


class BidRequestAdmin(admin.ModelAdmin):
    list_display = ["id",
                    "external_id",
                    "imp",
                    "click",
                    "conv",
                    "site",
                    "ssp_id",
                    "user_id"]
    
    actions = ['delete_selected']
