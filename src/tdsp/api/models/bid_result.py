from django.db import models


class BidResult(models.Model):
    win = models.BooleanField( default=False )
    price = models.FloatField(default=None, null=True)
    click = models.FloatField(default=None, null=True)
    conv = models.FloatField(default=None, null=True)
    revenue = models.FloatField(default=None, null=True)
    external_id = models.CharField(max_length=255, default="")

    class Meta:
        verbose_name_plural = "BidResult"

    def __str__(self) -> str:
        return self.name

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