from django.views.generic import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

import json

from api.models import (BidResult, History, Config, SspUser)
from api.tools.http_tools import error_status
from api.tools.logging_tools import error_log, info_log


class NotifyView(View):
    
    @staticmethod
    def _send_response():
        return HttpResponse("",
                            status=200,
                            content_type="text/plain;charset=UTF-8")

    @staticmethod
    def _init_bud_result(data: dict):
        if data['win']:
            bid = BidResult.objects.create(win=data['win'],
                                           price=data['price'],
                                           click=data['click'],
                                           conv=data['conversion'],
                                           revenue=data['revenue'],
                                           external_id=data['id'])
        else:
            bid = BidResult.objects.create(win=data['win'],
                                           external_id=data['id'])
        bid.save()
        return bid

 

    @staticmethod
    def _win_notify(data: dict, history: History):
        campaign = history.bid_response.creative.campaign
        campaign.budget -= float(data['price'])
        campaign.save()

        config = Config.objects.last()
        config.budget -= float(data['price'])
        config.budget = round(config.budget, 2)
        info_log(str(config.budget))
        config.total_revenue += float(data['revenue'])
        config.total_revenue = round(config.total_revenue, 2)
        config.save()
        try:
            ssp_user = SspUser.objects.get(Q(user_id=history.bid_request.user_id) & Q(creative=history.bid_response.creative))
            ssp_user.frequency_capping += 1
            ssp_user.save()
        except ObjectDoesNotExist as e:
            error_log(str(e))
    
    @staticmethod
    def _check_history(data: dict):
        if not History.objects.filter(bid_result__external_id=data['id']).exists():
            try:
                history = History.objects.get(bid_request__external_id = data['id'])
                return history, True
            except Exception as e:
                error_log(str(e))
                return None, False

        return None, False
    
    @csrf_exempt
    def post(self, request):
        
        data = json.loads(request.body)
        info_log("Notify: " + str(data))
        
        history, exists = self._check_history(data)
        if exists and history is not None:
            try:
                history.bid_result =  self._init_bud_result(data)
                history.save()
                if data['win']:
                    self._win_notify(data, history)
            except ObjectDoesNotExist as e:
                error_log(str(e))
            return self._send_response()
        else:
            return error_status("", 400)
