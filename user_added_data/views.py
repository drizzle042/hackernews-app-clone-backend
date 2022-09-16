from django.views import View
from django.http import HttpResponse
from .serializers import SerializedData 


class AllData(View):

    def get(self, request):
        data = SerializedData.allData()
        return HttpResponse(data)
