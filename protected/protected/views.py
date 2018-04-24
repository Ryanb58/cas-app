from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


from django.contrib.auth import authenticate


@csrf_exempt
@require_http_methods(["GET", "POST"])
def login(request, next_page=None, required=False):
    """Forwards to Auth login URL or verifies header/cookie."""
    user = authenticate(request=request)
    if user and user.is_authenticated:
        if next_page:
            return HttpResponseRedirect(next_page)
        return HttpResponseRedirect('/')

    auth_service_url = 'http://localhost:8001/accounts/login/?next=http://localhost:8000/'

    return HttpResponseRedirect(auth_service_url)


@login_required
def logout(request):
    auth_service_url = 'http://localhost:8001/accounts/logout/?next=http://localhost:8000/'
    return HttpResponseRedirect(auth_service_url)


@login_required
def protected_page(request):
    return HttpResponse(
        "Welcome to the protected resource: {}".format(request.user.username))
