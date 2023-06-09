from django.views.generic import View
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile

import json
import base64

from ...models import UserModel, Creative, Campaign
from ...tools.http_tools import data_status, error_status, ok_status
from ...tools.jwt_tools import decode_jwt, generate_jwt


class UiCreativeView(View):

    @staticmethod
    def get_categories(data):
        cat = []
        for i in data['categories']:
            categ = Category.objects.filter(code=i['code']).first()  # type: ignore
            cat.append(categ)
        return set(cat)

    def get(self, request):
        user_info = decode_jwt(request)

        user = UserModel.objects.get(id=int(user_info['user_id']))
        if user:
            creatives = Creative.objects.all()
            data = []
            for creative in creatives:
                data.append(creative.as_dict())

            return data_status(data)
        else:
            return error_status("user not found", 400)

    def post(self, request):
        user_info = decode_jwt(request)
        try:
            user = UserModel.objects.get(id=int(user_info['user_id']))
        except:
            return error_status("user not found", 400)
        if user:
            try:
                data = json.loads(request.body)
                camp = Campaign.objects.get(id=data['campaign_id'])
                image_file = ContentFile(base64.b64decode(data['file']))
                creative = Creative.objects.create(
                    external_id=data['external_id'],
                    name = data['name'],
                    campaign = camp
                )
                cat = self.get_categories(data)
                creative.categories.set(cat)
                creative.image.save(data['external_id'] + ".png", image_file, save=True)
                creative.save()
                json_data = json.dumps(creative.as_dict())
                return HttpResponse(json_data,  # type: ignore
                                    status=200,
                                    content_type="application/json")
            except:
                return error_status("wrong params", 401)

    @staticmethod
    def check_view(request, id):
        user_info = decode_jwt(request)
        try:
            user = UserModel.objects.get(id=int(user_info['user_id']))
        except:
            return error_status("user not found", 400)
        if user:
            if request.method == "GET":
                return UiCreativeView.get_single(request, id)
            if request.method == "DELETE":
                return UiCreativeView.delete(request, id)
            if request.method == "PATCH":
                return UiCreativeView.edit(request, id)

    @staticmethod
    def delete(request, id):
        try:
            creative = Creative.objects.get(id=id)
        except ObjectDoesNotExist:
            return error_status("creative not found", 402)
        creative.delete()
        
        return ok_status()

    @staticmethod
    def get_single(request, id):
        try:
            creative = Creative.objects.get(id=id)
        except ObjectDoesNotExist:
            return error_status("creative not found", 402)
        
        return data_status(creative.as_dict())

    @staticmethod
    def edit(request, id):
        data = json.loads(request.body)
        try:
            item = Creative.objects.get(id=id)
        except ObjectDoesNotExist:
            return error_status("creative not found", 402)
        if "external_id" in data:
            item.external_id = data['external_id']
            item.save()
        elif "name" in data:
            item.name = data['name']
            item.save()
        elif "campaign" in data:
            item.campaign = data['campaign']
            item.save()
        elif "image" in data:
            image_file = ContentFile(base64.b64decode(data['image']))
            item.image.save(item.external_id + ".png", image_file, save=True)
            item.save()
        elif "categories" in data:
            cat = UiCreativeView.get_categories(data)
            item.categories.set(cat)
            item.save()
        
        return ok_status()    
