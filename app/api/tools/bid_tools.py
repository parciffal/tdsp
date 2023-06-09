from django.conf import settings

import requests
import random
import numpy as np
import os

from api.models import BidRequest, Creative, SspUser, Config, History, BidResult

from .logging_tools import error_log, info_log

TEAMS = int(os.environ["TEAMS"])

MATRIX = np.array([
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    [0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
    [0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2],
    [0.2, 0.3, 0.4, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3],
    [0.3, 0.4, 0.5, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4],
    [0.3, 0.4, 0.5, 0.8, 1.0, 1.1, 1.2, 1.3, 1.3, 1.5],
    [0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.3, 1.4, 1.5, 1.5],
    [0.4, 0.5, 0.6, 0.8, 1.0, 1.3, 1.3, 1.5, 1.5, 1.6],
    [0.5, 0.6, 0.7, 0.8, 0.9, 1.4, 1.4, 1.5, 1.6, 1.7],
    [0.5, 0.6, 0.8, 0.9, 1.3, 1.4, 1.5, 1.6, 1.7, 1.7],
])


class Analyzer:
    def __init__(self):
        self.config = Config.objects.last()
        self.aggressive = False
        self.total_budget = self.config.budget
        self.rounds_won = BidResult.objects.filter(win=True).count()
        self.rounds_played = BidRequest.objects.count()
        self.rounds_left = self.config.impressions_total - self.rounds_played
        # self.game_goal = self.config.game_goal  FIXME for CPC

        initial_budget = self.config.initial_budget

        self.avg_bid = (initial_budget * TEAMS) / self.config.impressions_total

        self.click_rev = self.config.click_revenue
        self.conv_rev = self.config.conversion_revenue
        self.history = History.objects.all()
        if self.config.auction_type == 2:
            self.avg_bid *= 1.3

    @staticmethod
    def easy_bid(click_prob, conv_prob, avg_bid, budget):

        x = int(click_prob * 10)
        y = int(conv_prob * 10)
        coef = MATRIX[y][x]
        bid = coef * avg_bid
        if bid > budget:
            bid = budget
        return float(bid)

    @staticmethod
    def user_exceed(user_id, creative):
        """
        Check if a SspUser has frequency_capping over 3 with the same creative
        """
        try:
            ssp_user = SspUser.objects.get(user_id=user_id, creative=creative)
        except SspUser.DoesNotExist:
            return False

        if ssp_user.frequency_capping >= 3:
            return True

    def set_aggr(self, aggressive):
        self.aggressive = aggressive

    @staticmethod
    def find_ssp_id(url, ssp_id):
        """
            find ssp ete false a gin@ petqa qchana
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                lines = response.text.split('\n')
                for line in lines:
                    if ssp_id in line:
                        print(f"SSD ID '{ssp_id}' found in the ads.txt file.")
                        return True
                else:
                    print(f"SSD ID '{ssp_id}' not found in the ads.txt file.")
                    return False
            else:
                print("Error fetching the ads.txt file.")
                return False
        except:
            return False

    def analyze(self, data, ads=False, freq=False):
        """
        This function analyzes incoming data and returns a response to be sent back to the client.

        Args:
        - data (dict): A dictionary containing the following keys:
            - 'bcat' (list): A list of strings representing the categories of the website.
            - 'ssp' (str): A string representing the Supply Side Platform.
            - 'site' (dict): A dictionary containing information about the site, with the following keys:
                - 'domain' (str): A string representing the domain of the site.
            - 'user' (dict): A dictionary containing information about the user, with the following keys:
                - 'id' (str): A string representing the user's ID.
            - 'click' (dict): A dictionary containing information about the click, with the following keys:
                - 'prob' (float): A float representing the probability of a click.
            - 'conv' (dict): A dictionary containing information about the conversion, with the following keys:
                - 'prob' (float): A float representing the probability of a conversion.
            - 'imp' (dict): A dictionary containing information about the impression, with the following keys:
                - 'banner' (dict): A dictionary containing information about the banner, with the following keys:
                    - 'w' (int): An integer representing the width of the banner.
                    - 'h' (int): An integer representing the height of the banner.
        - aggressive (bool): A boolean indicating whether to be more aggressive with bidding.

        Returns:
        - response (dict): A dictionary containing the following keys:
            - 'external_id' (str): A string representing the ID of the chosen creative.
            - 'price' (float): A float representing the bid price.
            - 'image_url' (str): A string representing the URL of the chosen creative's image.
            - 'cat' (list): A list of strings representing the categories of the chosen creative.
        - creative (Creative): An object representing the chosen creative.
        """
        bcat = data['bcat']
        ssp = data['ssp']
        domain = data['site']['domain']
        user_id = data['user']['id']
        click_prob = float(data['click']['prob'])
        conv_prob = float(data['conv']['prob'])

        info_log(f'\033[1;34m{self.total_budget=}\n{self.rounds_left=}\n{self.avg_bid=}\n{self.rounds_played=}\033[1;0m')
        self.config.played_rounds += 1
        self.config.save()

        creatives = Creative.objects \
            .exclude(categories__code__in=bcat) \
            .exclude(categories__super_category__code__in=bcat)

        if not creatives:
            return None, None


        won_creative_ids = [hr.bid_response.external_id for hr in
                            self.history.filter(bid_result__win=True, bid_request__user_id=user_id)]

        # available_creatives = [creative for creative in creatives if creative.external_id not in won_creative_ids]
        available_creatives = Creative.objects.exclude(external_id__in=won_creative_ids). \
            exclude(categories__code__in=bcat).exclude(categories__super_category__code__in=bcat)

        if available_creatives:
            creative = random.choice(available_creatives)
            rpt_coef = 1
        else:
            if freq:
                for creative in creatives:
                    if self.user_exceed(user_id, creative):
                        creatives.exclude(creative)
            try:
                creative = random.choice(creatives)
                rpt_coef = 0.7
            except:
                return None, None

        company = creative.campaign
        budget = company.budget

        if self.click_rev * 1.7 > self.conv_rev:
            bid = self.easy_bid(click_prob, conv_prob, self.avg_bid * 1.2, self.total_budget) * rpt_coef
        else:
            bid = self.easy_bid(click_prob, conv_prob, self.avg_bid, self.total_budget) * rpt_coef

        info_log(f'\033[1;33m{bid=}\033[1;0m')

        try:
            if self.rounds_played / self.rounds_won < TEAMS and click_prob >= 0.5:
                bid *= 1.2
        except ZeroDivisionError:
            bid *= 1.15

        # if ain't gonna receive revenue from impressions - just play for click
        if ads:
            if not self.find_ssp_id("http://" + os.environ["IP"] + ":" + os.environ["HOST_PORT"] + "/ads.txt?publisher=" + domain, ssp):
                bid = self.avg_bid * click_prob
        # cpc game
        """
        elif self.game_mode == "revenue":
            bid = self.avg_bid * click_prob
        """

        if bid > budget or self.rounds_left < 1:
            bid: float = budget


        width = int(data['imp']['banner']['w'])
        height = int(data['imp']['banner']['h'])

        category = [i.code for i in creative.categories.all()]

        image_url = 'media/creative/{}?width={}&height={}'.format(creative.id, width, height)
        
        response = {
            "external_id": creative.external_id,
            "price": round(bid, 2),
            "image_url": settings.ADS_SERVER + image_url,
            "cat": category
        }
        return response, creative
