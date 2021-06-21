from django.contrib.auth.middleware import AuthenticationMiddleware
from django.conf import settings

from core.database.database_tools import get_user

class CustomAuthMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE%s setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")
        request.user = get_user(request)


class RequestLogger:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code Before View

        response = self.get_response(request)
        
        # Code After View

        return response

    def process_request(self, request):
        print("hello, it is process request")

    def process_view(self, request, view_func, view_args, view_kwargs):
        print("hello, it is process view")

    def process_response(self, response):
        print("hello, it is process response")