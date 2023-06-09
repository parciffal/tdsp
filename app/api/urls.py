from django.urls import path
 
from .views import *
#readme.so

urlpatterns = [
    path('rtb/bid/', BidView.as_view()),
    path('rtb/notify/', NotifyView.as_view()),
    path('game/configure/', ConfigView.as_view()),
    path('api/creatives/', CreativeView.as_view()),
    path('api/campaigns/', CampaignView.as_view()),
    # path('ui/creative/<int:id>/', UiCreativeView.check_view),
    # path('ui/creative/', UiCreativeView.as_view()),
    # path('ui/campaign/<int:id>/', UiCampaignView.check_view),
    # path('ui/campaign/', UiCampaignView.as_view()),
    # path('auth/login', UserAuthView.login),
    # path('auth/logout', UserAuthView.logout),
    # path('auth/info', UserAuthView.user_info),
    path('bid_analyzer/', bid_analyzer_view, name='bid_analyzer'),
    
] 
