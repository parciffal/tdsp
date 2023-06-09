#
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.html import mark_safe


class UserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.get_username()

    def as_json(self):
        data = {}
        dct = self.user.__dict__
        keys_not_in = ['_state', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined']
        for k in dct.keys():
            if dct[k] is not None and k not in keys_not_in:
                if dct[k] != "":
                    data[k] = dct[k]
        return data


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_user']

    def get_user(self, obj: UserModel):
        link = "/admin/auth/user/{}/change/".format(obj.user.id)
        kil = """<a href="{}">{}</a>""".format(link, obj.user.get_username())
        return mark_safe(kil)
