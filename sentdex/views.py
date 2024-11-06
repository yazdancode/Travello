from django.shortcuts import render
from django.views import View
from sentdex.models import Destination, DetailedDescription
from django.core.exceptions import ObjectDoesNotExist

class DestinationView(View):
    template_name = 'sentdex/index.html'
    
    def get_destinations_with_descriptions(self):
        dest1 = []
        for i in range(6):
            try:
                temp = DetailedDescription.objects.get(dest_id=(i + 1) * 2)
                dest1.append(temp)
            except ObjectDoesNotExist:
                dest1.append(None)
        return dest1

    def get(self, request):
        dests = Destination.objects.all()
        dest1 = self.get_destinations_with_descriptions()
        return render(request, self.template_name, {'dests': dests, 'dest1': dest1})