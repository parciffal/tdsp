from django.db import models
from django.contrib import admin


class Campaign(models.Model):
    name = models.CharField(max_length=255, default="")
    budget = models.FloatField(default=0)
    is_active = models.BooleanField(default=False)
    frequency_capping = models.IntegerField(default=0)
    bid_floor = models.FloatField(default=0)
    played_games = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Campaign"

    def __str__(self) -> str:
        return str(self.name)

    def as_json(self) -> dict:
        data = {
            "id": self.id,
            "name": self.name,
            "budget": self.budget,
            "is_active": self.is_active,
            "frequency_capping": self.frequency_capping,
            "bid_floor": self.bid_floor,
            "played_games": self.played_games
        }
        return data


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['id',
                    "is_active",
                    "budget",
                    "name",
                    "frequency_capping",
                    "bid_floor",
                    "played_games"]

    actions = ['delete_selected']
