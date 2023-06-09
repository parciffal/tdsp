from django.db import models

from .category import Category

class BidResponse(models.Model):
    external_id = models.CharField(max_length=255, default=None, null=True)
    image_url = models.TextField(default=None, null=True)
    price = models.FloatField(default=None, null=True)
    categories = models.ManyToManyField(Category, on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = "BidResponse"

    def __str__(self) -> str:
        return self.name

    def as_json(self):
        data = {
            "id": self.id,
            "external_id": self.external_id,
            "image_url": self.image_url,
            "price": self.price,
            "categories": self.categories,
        }
        return data