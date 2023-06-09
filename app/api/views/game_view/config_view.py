from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile

import base64
import json

from api.models import *
from api.tools.http_tools import ok_status
from api.tools.free_mode_config import FREE_MODE_CONFIG
from api.tools.logging_tools import info_log


class ConfigView(View):
    
    @staticmethod
    def _clear_database():
        Config.objects.all().delete()
        Campaign.objects.all().delete()
        History.objects.all().delete()
        Creative.objects.all().delete()
        BidRequest.objects.all().delete()
        BidResponse.objects.all().delete()
        BidResult.objects.all().delete()

    @staticmethod
    def _init_free_campaign(data) -> Campaign:

        campaign_data = FREE_MODE_CONFIG['campaign']
        campaign = Campaign.objects.create(
            name=campaign_data['name'],
            budget=data['budget'],
            is_active=campaign_data['is_active'],
            frequency_capping=data['frequency_capping'],
            bid_floor=0.1,
            played_games=0)
        campaign.save()
        
        return campaign

    @staticmethod
    def _init_free_creatives(campaign: Campaign) -> None:
        creatives_data = FREE_MODE_CONFIG['creatives']

        categories = Category.objects.all().filter(super_category=None)
        for item in creatives_data:
            file_data = ContentFile(base64.b64decode(item['base64png']))

            creative = Creative.objects.create(external_id=item['external_id'],
                                                name=item['name'],
                                                campaign=campaign)

            creative.categories.set(categories)
            creative.image.save(str(creative.id) + ".png", file_data, save=True)
            creative.save()


    def _init_config(self, data):
        if data['mode'] == 'free':
            campaign = self._init_free_campaign(data)
            self._init_free_creatives(campaign)
        
        Config.objects.create(
            impressions_total=data['impressions_total'],
            auction_type=data['auction_type'],
            mode=data['mode'],
            budget=data['budget'],
            initial_budget=data['budget'],
            impressions_revenue=data['impression_revenue'],
            click_revenue=data['click_revenue'],
            conversion_revenue=data['conversion_revenue'],
            frequency_capping=data['frequency_capping'])

    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        info_log("Config data: " + str(data))

        self._clear_database()
        self._init_config(data)
    
        return ok_status()
