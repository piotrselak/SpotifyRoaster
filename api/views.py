from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView



# class Authenticate(APIView):
#     @staticmethod
#     def get(request: HttpRequest) -> Response:
#         code = request.GET.get('code')
#         response = Response()
#         response.set_cookie('code', code)
#
