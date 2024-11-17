from django.contrib import admin

from sentdex.models import (
    Card,
    DailyPlan,
    Destination,
    DestinationImage,
    DetailedDescription,
    DetailedDescriptionImage,
    NetBanking,
    PassengerDetail,
    Transaction,
)

admin.site.register(Destination)
admin.site.register(DestinationImage)
admin.site.register(DetailedDescription)
admin.site.register(DetailedDescriptionImage)
admin.site.register(DailyPlan)
admin.site.register(PassengerDetail)
admin.site.register(Card)
admin.site.register(NetBanking)
admin.site.register(Transaction)
