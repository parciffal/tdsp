from django.db import models
from django.db.models.enums import Choices


class Config(models.Model):
    impressions_total = models.IntegerField(default=None, null=True)
    auction_type = models.IntegerChoices((1,2))
    mode = models.TextChoices(("free", "script"))
    budget = models.IntegerField(default=None, null=True)
    impressions_revenue = models.IntegerField(default=None, null=True)
    click_revenue = models.IntegerField(default=None, null=True)
    conversion_revenue = models.IntegerField(default=None, null=True)
    frequency_capping = models.IntegerField(default=None, null=True)
    

    class Meta:
        verbose_name_plural = "Config"

    def __str__(self) -> str:
        return self.name

    def as_json(self):
        data = {
            "id": self.id,
            "impressions_total": self.impressions_total,
            "auction_type": self.auction_type,
            "mode": self.mode,
            "budget": self.budget,
            "impressions_revenue": self.impressions_revenue,
            "click_revenue": self.click_revenue,
            "conversion_revenue": self.conversion_revenue,
            "frequency_capping": self.frequency_capping,
        }
        return data