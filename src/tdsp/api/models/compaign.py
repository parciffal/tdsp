from django.db import models


class Campaign(models.Model):
    name = models.CharField(max_length=255, default="")
    budget = models.IntegerField(default=None, null=True)
    is_active = models.BooleanField(default=False)
    external_id = models.CharField(max_length=255, default="")
    frequency_capping = models.FloatField(default=None, null=True)
    bid_floor = models.FloatField(default=None, null=True)

    class Meta:
        verbose_name_plural = "Campaign"

    def __str__(self) -> str:
        return self.name

    def as_json(self):
        data = {
            "id": self.id,
            "name": self.name,
            "budget": self.budget,
            "is_active": self.is_active
        }
        return data