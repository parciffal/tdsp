from django.views.generic import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

import json

from api.models import BidRequest 
from api.models import BidResponse, History, SspUser, Category
from api.tools.http_tools import error_status
from api.tools.bid_tools import Analyzer
from api.tools.logging_tools import error_log, info_log


class BidView(View):

    @staticmethod
    def _get_bid_categories(data):
        cat = []
        for i in data:
            try:
                categ = Category.objects.get(code=i)
                cat.append(categ)
            except ObjectDoesNotExist as e:
                error_log(str(e))
        return set(cat)

    @staticmethod
    def _init_bid_request(data: dict):
        bid_request = BidRequest.objects.create(external_id=data['id'],
                                                imp=str(data['imp']),
                                                click=data['click']['prob'],
                                                conv=data['conv']['prob'],
                                                site=data['site']['domain'],
                                                ssp_id=data['ssp']['id'],
                                                user_id=data['user']['id'])

        bid_request.categories.set(BidView._get_bid_categories(data['bcat']))
        bid_request.save()

        return bid_request

    @staticmethod
    def _init_bid_response(data: dict, bid_request, creative):
        bid_response = BidResponse.objects.create(bid_request=bid_request,
                                                  external_id=data['external_id'],
                                                  image_url=data['image_url'],
                                                  price=data['price'],
                                                  creative=creative)
        bid_response.categories.set(bid_response.creative.categories.all())
        bid_response.save()
        return bid_response

    @staticmethod
    def _check_request(data):
        return not BidRequest.objects.filter(external_id=data['id']).exists()

    @csrf_exempt
    def _send_response(self, bid_data, bid_request, creative, data):
        history = History.objects.create(bid_request=bid_request)
        if bid_data is None:
            bid_response = BidResponse.objects.create(bid_request=bid_request)

            history.bid_response = bid_response
            history.save()

            info_log("Bid response: No bid")
            return HttpResponse("No bid",
                                status=204,
                                content_type="text/plain;charset=UTF-8")
        else:
            bid_response = self._init_bid_response(bid_data, bid_request, creative)

            history.bid_response = bid_response
            history.save()

            bid_data['price'] = round(bid_data['price'], 2)

            info_log("Bid response: " + str(bid_data))

            self._init_ssp_user(data, creative)
            return HttpResponse(json.dumps(bid_data),
                                status=200,
                                content_type="application/json")

    @staticmethod
    def _init_ssp_user(data, creative):
        if SspUser.objects.filter(Q(user_id=data['user']['id']) & Q(creative=creative)).__len__() == 0:
            ssp_user = SspUser.objects.create(
                user_id=data['user']['id'],
                creative=creative)
            ssp_user.save()

    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        info_log("Bid data: " + str(data))
        if self._check_request(data):
            bid_request = self._init_bid_request(data)
            bid_data, creative = Analyzer().analyze(data)
            return self._send_response(bid_data, bid_request, creative, data)
        error_log("Error 400: Bid already existed")
        return error_status("Bid already existed", 400)
