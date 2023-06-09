from django.db import models
from django.contrib import admin
from django.utils.safestring import mark_safe

from .creative_model import Creative


class SspUser(models.Model):
    user_id = models.CharField(max_length=255, null=True)
    creative = models.ForeignKey(Creative, on_delete=models.CASCADE, null=True, blank=True)
    frequency_capping = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Ssp_user"

    def __str__(self) -> str:
        return str(self.user_id)

    def as_json(self):
        data = {
            "id": self.id,  # type: ignore
            "user_id": self.user_id,
            "frequency_capping": self.frequency_capping
        }
        if self.creative:
            data["creative"] = self.creative.as_json()
        return data


class SspUserAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'user_id',
                    "frequency_capping",
                    "to_creative"]

    actions = ['delete_selected']

    def to_creative(self, obj: SspUser):
        if obj.creative:
            link = "/admin/api/creative/{}/change/".format(obj.creative.id)  # type: ignore
            kil = """<a href="{}">{}</a>""".format(link, obj.creative.name)
            return mark_safe(kil)
