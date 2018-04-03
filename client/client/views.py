from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required

class GreetingView(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)
