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

    auth_service_url = 'http://localhost:8001/accounts/login?next=http://localhost:8000/'

    # if not next_page:
    #     next_page = '/'

    return HttpResponseRedirect(auth_service_url)

    # backward compability for django < 2.0
    # is_user_authenticated = False

    # if sys.version_info >= (3, 0):
    #     bool_type = bool
    # else:
    #     bool_type = types.BooleanType

    # if isinstance(request.user.is_authenticated, bool_type):
    #     is_user_authenticated = request.user.is_authenticated
    # else:
    #     is_user_authenticated = request.user.is_authenticated()

    # if is_user_authenticated:
    #     return HttpResponseRedirect(next_page)


@login_required
def protected_page(request):
    return HttpResponse(
        "Welcome to the protected resource: {}".format(request.user.username))
