from django.conf import settings as django_settings
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View

from .config import settings


class OAuth2View(View):
    def get(self, request):
        """
        Handles the redirect from ADFS to our site.
        We try to process the passed authorization code and login the user.

        Args:
            request (django.http.request.HttpRequest): A Django Request object
        """
        code = request.GET.get("code", None)

        user = authenticate(authorization_code=code)

        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to the "after login" page.
                # Because we got redirected from ADFS, we can't know where the
                # user came from.
                if settings.LOGIN_REDIRECT_URL:
                    return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    return redirect(django_settings.LOGIN_REDIRECT_URL)
            else:
                # Return a 'disabled account' error message
                return render(request, "auth_adfs/disabled.html", status=403)
        else:
            # Return an 'invalid login' error message
            return render(request, "auth_adfs/login_failed.html", status=401)
