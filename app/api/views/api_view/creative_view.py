from django.views.generic import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.base import ContentFile

import base64
import json

from api.tools.logging_tools import error_log, info_log

from api.tools.http_tools import error_status
from api.models import Campaign, Creative, Category


class CreativeView(View):

    @staticmethod
    def _get_categories(data):
        cat = []
        for i in data['categories']:
            try:
                cat.append(Category.objects.get(code=i['code']))
            except:
                pass
        return set(cat)

    @staticmethod
    def _create_creative(data, campaign, categories):
        creative = Creative.objects.create(
            external_id=data['external_id'],
            name=data['name'],
            campaign=campaign)

        file_data = ContentFile(base64.b64decode(data['file']))

        creative.categories.set(categories)
        creative.image.save(str(creative.id) + ".png", file_data, save=True)
        creative.save()

        return creative

    @staticmethod
    def _creative_to_json(creative: Creative, categories: set, campaign: Campaign):
        category_data = [{"id": i.id, "code": i.code} for i in categories]
        creative_data = creative.as_json()

        return json.dumps({"id": creative_data['id'],
                           "external_id": creative_data['external_id'],
                           "name": creative_data['name'],
                           "campaign": {"id": campaign.id, "name": campaign.name},
                           "categories": category_data,
                           "url": settings.ADS_SERVER + creative_data['url']})

    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)

        info_log(str(data))
        if Creative.objects.filter(external_id=data['external_id']).__len__() == 0:

            campaign = Campaign.objects.get(pk=data['campaign']['id'])
            categories = self._get_categories(data)
            creative = self._create_creative(data, campaign, categories)
            json_data = self._creative_to_json(creative, categories, campaign)

            return HttpResponse(json_data,  # type: ignore
                                status=201,
                                content_type="application/json")
        error_log("Error 400: creative with external_id () exists".format(data['external_id']))
        return error_status("creative with external_id () exists".format(data['external_id']), 400)
