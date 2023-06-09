from django.db import models
from django.contrib import admin


class BidResult(models.Model):
    win = models.BooleanField(default=False)
    price = models.FloatField(default=None, null=True)
    click = models.FloatField(default=None, null=True)
    conv = models.FloatField(default=None, null=True)
    revenue = models.FloatField(default=None, null=True)
    external_id = models.CharField(max_length=255, default=None, null=True, unique=True)

    class Meta:
        verbose_name_plural = "BidResult"

    def __str__(self):
        return str(self.external_id)

    def as_json(self):
        data = {
            "id": self.id,
            "external_id": self.external_id,
            "price": self.price,
            "click": self.click,
            "conv": self.conv,
            "revenue": self.revenue,
            "win": self.win
        }
        return data


class BidResultAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'external_id',
                    "price",
                    "click",
                    "conv",
                    "revenue",
                    "win"]
    
    actions = ['delete_selected']
