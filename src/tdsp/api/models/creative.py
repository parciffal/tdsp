from django.db import models

from .category import Category
from .compaign import Campaign

class Creative(models.Model):
    external_id = models.CharField(max_length=255, default="")
    name = models.CharField(max_length=255, default="")
    categories = models.ManyToManyField(Category, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Creative"

    def __str__(self) -> str:
        return self.name

    def as_json(self):
        data = {
            "id": self.id,
            "external_id": self.external_id,
            "name": self.name,
            "categories": self.categories,
            "campaign": self.campaign
        }
        return data