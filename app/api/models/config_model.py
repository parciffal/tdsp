from django.db import models
from django.contrib import admin


class Config(models.Model):
    class AuctionType(models.IntegerChoices):
        FIRSTPRICE = 1, "First Price"
        SECONDPRICE = 2, "Second Price"

    class ModeChoices(models.TextChoices):
        FREE = "free", "Free"
        SCRIPT = 'script', "Script"

    game_goal = models.IntegerField(default=0)

    total_revenue = models.FloatField(default=0)
    # roundneri qanak
    impressions_total = models.IntegerField(default=0)

    played_rounds = models.IntegerField(default=0)

    auction_type = models.IntegerField(
        choices=AuctionType.choices,
        default=AuctionType.SECONDPRICE)

    mode = models.TextField(
        choices=ModeChoices.choices,
        default=ModeChoices.FREE)

    budget = models.FloatField(default=0)
    initial_budget = models.FloatField(default=0)
    # minimal poxna vor karas stanas bidic

    impressions_revenue = models.IntegerField(default=0)

    click_revenue = models.IntegerField(default=0)

    conversion_revenue = models.IntegerField(default=0)
    # qani angam user@ kara tena creativ@
    frequency_capping = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Config"

    def __str__(self) -> str:
        return str(self.as_json())

    def as_json(self) -> dict:
        data = {
            "id": self.id,
            "impressions_total": self.impressions_total,
            "auction_type": self.auction_type,
            "mode": self.mode,
            "budget": self.budget,
            "impressions_revenue": self.impressions_revenue,
            "played_rounds": self.played_rounds,
            "click_revenue": self.click_revenue,
            "conversion_revenue": self.conversion_revenue,
            "frequency_capping": self.frequency_capping,
        }
        return data


class ConfigAdmin(admin.ModelAdmin):
    list_display = ['id',
                    "impressions_total",
                    "auction_type",
                    "mode",
                    "budget",
                    "impressions_revenue",
                    "played_rounds",
                    "click_revenue",
                    "conversion_revenue",
                    "frequency_capping",
                    "total_revenue", 
                    "initial_budget",
					]

    actions = ['delete_selected']
