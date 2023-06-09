from django.db import models
from django.contrib import admin
from django.utils.safestring import mark_safe

from .category_model import Category
from .compaign_model import Campaign
 

class Creative(models.Model):
    
    external_id = models.CharField(max_length=255, default="", unique=True)
    name = models.CharField(max_length=255, default="")
    categories = models.ManyToManyField(Category)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="creative/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Creative"

    def __str__(self) -> str:
        return str(self.name)

    def as_json(self) -> dict:
        data = {
            "id": self.id,
            "external_id": self.external_id,
            "name": self.name,
            "categories": self.categories,
            "campaign": self.campaign,
            "url": self.image.url
        }
        return data


class CreativeAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'external_id',
                    "name",
                    "to_campaign",
                    "image"]
    
    actions = ['delete_selected']
    
    def to_campaign(self, obj: Campaign):
        link = "/admin/api/campaign/{}/change/".format(obj.campaign.id)
        kil = """<a href="{}">{}</a>""".format(link, obj.campaign.name)
        return mark_safe(kil)
