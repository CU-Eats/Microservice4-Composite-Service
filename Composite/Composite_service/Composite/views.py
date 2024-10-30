import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

@csrf_exempt
@require_http_methods(["GET"])
def composite_endpoint(request):
    try:
        input_data = json.loads(request.body)
        # Process input data and call other service here
        # Example call to another service
        response = requests.post(f"{settings.OTHER_SERVICE_BASE_URL}/api/other-endpoint/", json=input_data)
        return JsonResponse(response.json(), safe=False, status=response.status_code)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)