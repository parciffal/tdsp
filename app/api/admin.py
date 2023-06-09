from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserModel, UserAdmin)

admin.site.register(BidRequest, BidRequestAdmin)
admin.site.register(BidResponse, BidResponseAdmin)
admin.site.register(BidResult, BidResultAdmin)

admin.site.register(History, HistoryAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(SspUser, SspUserAdmin)

admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Config, ConfigAdmin)
admin.site.register(Creative, CreativeAdmin)

