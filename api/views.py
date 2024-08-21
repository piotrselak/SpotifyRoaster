from rest_framework.response import Response
from rest_framework.views import APIView


class RoastOperations(APIView):
    @staticmethod
    def get(request) -> Response:
        return Response("Hello World2")
