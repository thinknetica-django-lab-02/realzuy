import re

from django.http import HttpRequest, HttpResponse


class MyMobileLayoutMiddleware:
    """Определяет, является ли клиент мобильным приложением."""
    def __init__(self, get_response: HttpRequest) -> None:
        self._get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            request.is_mobile = True
        else:
            request.is_mobile = False

        response = self._get_response(request)
        return response
