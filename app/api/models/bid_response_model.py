from django.db import models
from django.contrib import admin
from django.utils.html import mark_safe

from .creative_model import Creative
from .category_model import Category
from .bid_request_model import BidRequest

class BidResponse(models.Model):
    bid_request = models.ForeignKey(BidRequest, on_delete=models.CASCADE, blank=True, null=True)
    external_id = models.CharField(max_length=255, default=None, null=True)
    image_url = models.TextField(default=None, null=True)
    price = models.FloatField(default=None, null=True)
    categories = models.ManyToManyField(Category)
    creative = models.ForeignKey(Creative, on_delete=models.CASCADE, default=None, null=True)

    class Meta:
        verbose_name_plural = "BidResponse"

    def __str__(self):
        return str(self.external_id)

    def as_json(self):
        data = {
            "id": self.id,
            "external_id": self.external_id,
            "image_url": self.image_url,
            "price": self.price,
            "categories": self.categories,
            "bid_request": self.bid_request.as_json()
        }
        if self.creative:
            data['creative'] = self.creative.as_json()
        return data


class BidResponseAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'external_id',
                    'image_url',
                    'price',
                    'to_bid_request',
                    'to_creative']
    
    actions = ['delete_selected']
    
    def to_bid_request(self, obj: BidResponse):
        link = "/admin/api/bidrequest/{}/change/".format(obj.bid_request.id)
        kil = """<a href="{}">{}</a>""".format(link, obj.bid_request.external_id)
        return mark_safe(kil)

    def to_creative(self, obj: BidResponse):
        link = "/admin/api/creative/{}/change/".format(obj.creative.id)
        kil = """<a href="{}">{}</a>""".format(link, obj.creative.external_id)
        return mark_safe(kil)

