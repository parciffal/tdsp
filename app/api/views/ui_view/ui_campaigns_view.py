from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist

import json

from ...models import UserModel, Campaign
from ...tools.http_tools import data_status, error_status, ok_status
from ...tools.jwt_tools import decode_jwt


class UiCampaignView(View):

    def get(self, request):
        user_info = decode_jwt(request)
        try:
            user = UserModel.objects.get(id=int(user_info['user_id']))
        except:
            return error_status("user not found", 400)
        if user:
            campaigns = Campaign.objects.all()

            data = []
            for campaign in campaigns:
                data.append(campaign.as_dict())

            return data_status(data)
        

    def post(self, request):
        user_info = decode_jwt(request)
        try:
            user = UserModel.objects.get(id=int(user_info['user_id']))
        except:
            return error_status("user not found", 400)
        if user:
            try:
                data = json.loads(request.body)

                campaign = Campaign.objects.create(name=data['name'],  # type: ignore
                                                budget=data['budget'],
                                                is_active=True)

                campaign.save()
                return ok_status()
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
                return UiCampaignView.get_single(request, id)
            if request.method == "DELETE":
                return UiCampaignView.delete(request, id)
            if request.method == "PATCH":
                return UiCampaignView.edit(request, id)

    @staticmethod
    def delete(request, id):
        try:
            campaign = Campaign.objects.get(id=id)
        except ObjectDoesNotExist:
            return error_status("creative not found", 402)
        campaign.delete()
        
        return ok_status()

    @staticmethod
    def get_single(request, id):
        try:
            campaign = Campaign.objects.get(id=id)
        except ObjectDoesNotExist:
            return error_status("creative not found", 402)
        
        return data_status(campaign.as_dict())

    @staticmethod
    def edit(request, id):
        data = json.loads(request.body)
        try:
            item = Campaign.objects.get(id=id)
        except ObjectDoesNotExist:
            return error_status("creative not found", 402)
        if "name" in data:
            item.name = data['name']
            item.save()
        elif "is_active" in data:
            item.is_active = data['is_active']
            item.save()
        elif "budget" in data:
            item.budget = data['budget']
            item.save()
        
        return ok_status()    
