import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def call_get_food_items_by_restaurant(request, restaurant_name):
    try:
        # Construct the endpoint URL with the restaurant name
        endpoint_url = f"{settings.RESTAURANT_URL}/restaurant/getMenu/{restaurant_name}/"

        # Make the GET request
        response = requests.get(endpoint_url, timeout=10)

        # Check response and return data
        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        else:
            return JsonResponse({'error': 'Failed to fetch menu'}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def call_add_food_item(request):
    if request.method == 'POST':
        # Extract data from the request body
        body = json.loads(request.body)

        data = {
            "restaurant": body.get("restaurant"),
            "name": body.get("name"),
            "price": body.get("price"),
            "calorie": body.get("calorie"),
            "description": body.get("description", ""),
            "is_available": body.get("is_available", True)
        }

        try:
            # URL for the add_food_item endpoint
            endpoint_url = f"{settings.RESTAURANT_URL}/restaurant/add/"

            # Make the POST request with the data
            response = requests.post(endpoint_url, json=data, timeout=10)

            # Check and return the response from the other service
            if response.status_code == 201:
                return JsonResponse(response.json(), status=201)
            else:
                return JsonResponse(response.json(), status=response.status_code)

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)