from django.contrib import admin

from sentdex.models import (
    Destination,
    DestinationImage,
    DetailedDescription,
    DetailedDescriptionImage,
    DailyPlan,
)


admin.site.register(Destination)
admin.site.register(DestinationImage)
admin.site.register(DetailedDescription)
admin.site.register(DetailedDescriptionImage)
admin.site.register(DailyPlan)
