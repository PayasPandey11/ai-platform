import jwt
from django.http import JsonResponse
import sys, os


def validate(function):
    """Decorator to validate JWT token. file location-woohoonlu/decorators.py

    Args: function/view.

    Returns: Function(request,userId) if validation successful, Status 401 if not successful
    """

    def wrap(request, *args, **kwargs):
        key = "woohooenterprisesecret"
        try:
            domainId = request.META['HTTP_AUTHORIZATION']
            request.uid = domainId
            return function(request, *args)

        except TypeError as e:
            print(e)
            response = dict(success=False, message="Validation error", error=str(e))
            return JsonResponse(response, status=500)
        # except KeyError as e:
        #      response = dict(success=False, message="key error", error=str(e))
        #      return JsonResponse(response, status=401)
        # except :
        #     response = dict(success=False, message="server error", error=str("Unknown error"))
        #     return JsonResponse(response, status=401)


    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
