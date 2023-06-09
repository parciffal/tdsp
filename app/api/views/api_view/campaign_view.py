from django.views.generic import View
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

import json

from api.tools.http_tools import error_status
from api.tools.logging_tools import *
from api.models import Campaign


class CampaignView(View):

    @staticmethod
    def _send_response(campaign: Campaign):
        campaign_data = json.dumps(campaign.as_json())

        return HttpResponse(campaign_data,  # type: ignore
                            status=201,
                            content_type="application/json")

    @csrf_exempt
    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        info_log(str(data))
        try:
            campaign = Campaign.objects.create(name=data['name'],
                                               budget=data['budget'],
                                               is_active=True)
            return self._send_response(campaign)
        except Exception as e:
            error_message = "Campaign init error"
            error_code = 400
            error_log("Error {}: {}".format(error_code, error_message))
            return error_status(error_message, 400)
