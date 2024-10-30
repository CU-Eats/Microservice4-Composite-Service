from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.http import JsonResponse
from django.conf import settings


class LoginUserView(APIView):

    def post(self, request):
        # Define the URL to the external service
        URL = f'{settings.USER_SERVICE_HOST}/users/get_one_user/'

        # Extract parameters from the request data
        payload = request.data  # Access JSON data in POST request

        # Check if both 'uni' and 'password' parameters are provided
        if 'uni' not in payload or 'password' not in payload:
            return Response(
                {"error": "Please provide both 'uni' and 'password' parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        query_params = {
            'uni': payload['uni'],
            'password': payload['password']
        }

        try:
            # Make the POST request with JSON payload
            response = requests.get(URL, params=query_params)

            # Handle specific response status codes
            if response.status_code == 401:
                return Response(response.json(), status=status.HTTP_401_UNAUTHORIZED)

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)

            if response.status_code == 404:
                return Response(response.json(), status=status.HTTP_404_NOT_FOUND)

            # For other status codes, return a generic error message
            return Response(
                {"error": f"Request failed with status {response.status_code}: {response.text}"},
                status=response.status_code
            )

        except requests.RequestException as e:
            # Handle network errors or other request issues
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateUserView(APIView):

    def post(self, request):
        URL = f'{settings.USER_SERVICE_HOST}/users/add_user/'

        payload = request.data

        required_fields = ['uni', 'email', 'first_name', 'last_name', 'id_type', 'password']
        missing_fields = [field for field in required_fields if field not in payload]

        if missing_fields:
            return Response(
                {"error": f"Missing fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            'uni': payload['uni'],
            'email': payload['email'],
            'first_name': payload['first_name'],
            'last_name': payload['last_name'],
            'id_type': payload['id_type'],
            'password': payload['password']
        }

        try:
            response = requests.post(URL, json=data)

            if response.status_code == 201:
                return Response(response.json(), status=status.HTTP_201_CREATED)

            if response.status_code == 400:
                return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {"error": f"Request failed with status {response.status_code}: {response.text}"},
                status=response.status_code
            )

        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

