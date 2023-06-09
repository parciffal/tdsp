from django.db import models
from django.contrib import admin
from django.utils.safestring import mark_safe


class Category(models.Model):
    code = models.CharField(max_length=255, default="", unique=True)
    name = models.CharField(max_length=255, default="")
    super_category = models.ForeignKey("self", default=None, null=True, on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name_plural = "Category"

    def __str__(self) -> str:
        return str(self.name)

    def as_json(self) -> dict:
        data = {
            "id": self.id,
            "code": self.code,
            "name": self.name,
        }
        if self.super_category:
            data['super_category'] = self.super_category.as_json()
        return data


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'code',
                    'name',
                    'to_super_category']

    actions = ['delete_selected']

    def to_super_category(self, obj: Category):
        if obj.super_category : 
            link = "/admin/api/category/{}/change/".format(obj.super_category.id)
            kil = """<a href="{}">{}</a>""".format(link, obj.super_category.name)
            return mark_safe(kil)
