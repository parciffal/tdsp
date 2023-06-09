from django.db import models

from .category import Category

class BidRequest(models.Model):
    external_id = models.CharField(max_length=255, default=None, null=True)
    imp = models.TextField(default=None, null=True)
    click = models.FloatField(default=None, null=True)
    conv = models.FloatField(default=None, null=True)
    site = models.TextField(default=None, null=True)
    ssp_id = models.models.CharField(max_length=255, default=None, null=True)
    user_id = models.CharField(max_length=255, default=None, null=True)
    categories = models.ManyToManyField(Category, on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = "BidRequest"

    def __str__(self) -> str:
        return self.name

    def as_json(self):
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