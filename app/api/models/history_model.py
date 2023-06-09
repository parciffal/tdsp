from django.db import models
from django.contrib import admin
from django.utils.html import mark_safe

from .bid_request_model import BidRequest
from .bid_response_model import BidResponse
from .bid_result_model import BidResult


class History(models.Model):
    bid_request = models.OneToOneField(BidRequest, 
                                       on_delete=models.CASCADE, 
                                       blank=True,
                                       null=True)
    bid_response = models.OneToOneField(BidResponse,
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        null=True)
    bid_result = models.OneToOneField(BidResult, 
                                      on_delete=models.CASCADE, 
                                      blank=True, 
                                      null=True)

    class Meta:
        verbose_name_plural = "History"

    def __str__(self) :
        return "History"

    def as_json(self) -> dict:
        data = {
            "id": self.id,
            "bid_request": self.bid_request.as_json(),
            "bid_response": self.bid_response.as_json(),
            "bid_result": self.bid_result.as_json()
        }
        return data


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'to_bid_request',
                    "to_bid_response",
                    "to_bid_result"]
    
    actions = ['delete_selected']

    def to_bid_result(self, obj: History):
        link = "/admin/api/bidresult/{}/change/".format(obj.bid_result.id)
        kil = """<a href="{}">{}</a>""".format(link, obj.bid_result.external_id)
        return mark_safe(kil)

    def to_bid_response(self, obj: History):
        link = "/admin/api/bidresponse/{}/change/".format(obj.bid_response.id)
        kil = """<a href="{}">{}</a>""".format(link, obj.bid_response.external_id)
        return mark_safe(kil)
    
    def to_bid_request(self, obj: History):
        link = "/admin/api/bidrequest/{}/change/".format(obj.bid_request.id)
        kil = """<a href="{}">{}</a>""".format(link, obj.bid_request.external_id)
        return mark_safe(kil)
