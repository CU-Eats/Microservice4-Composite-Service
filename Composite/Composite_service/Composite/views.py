from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

# Create your views here.

@api_view(['GET'])
def get_menu(request, restaurant):
    url = f"http://localhost:8000/restaurant/everything"
    response = requests.get(url)
    if response.status_code == 200:
        menu_items = [item for item in response.json() if item['restaurant'] == restaurant]
        return Response(menu_items, status=status.HTTP_201_CREATED)
    return Response({"error": "Could not retrieve menu"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def place_order(request):
    user_id = request.data.get('user_id')
    restaurant = request.data.get('restaurant')
    items = request.data.get('items')  # List of food item names

    # Step 1: Verify User
    user_url = f"http://localhost:8000/user/{user_id}/"
    user_response = requests.get(user_url)
    if user_response.status_code != 200:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Step 2: Fetch Menu to verify items
    menu_url = f"http://localhost:8000/restaurant/everything"
    menu_response = requests.get(menu_url)
    if menu_response.status_code != 200:
        return Response({"error": "Could not retrieve menu"}, status=status.HTTP_400_BAD_REQUEST)

    available_items = {item['name']: item for item in menu_response.json() if
                       item['restaurant'] == restaurant and item['is_available']}
    ordered_items = [available_items[name] for name in items if name in available_items]
    if len(ordered_items) != len(items):
        return Response({"error": "Some items are not available"}, status=status.HTTP_400_BAD_REQUEST)

    # Step 3: Create Order
    order_url = "http://localhost:8000/order/create"
    order_data = {
        "user_id": user_id,
        "restaurant": restaurant,
        "items": ordered_items,
        "total": sum(item['price'] for item in ordered_items)
    }
    order_response = requests.post(order_url, json=order_data)
    if order_response.status_code == 201:
        return Response(order_response.json(), status=status.HTTP_201_CREATED)
    return Response({"error": "Failed to place order"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_user_order_history(request, user_id):
    # Retrieve user info
    user_url = f"http://localhost:8000/user/{user_id}/history"
    user_response = requests.get(user_url)
    if user_response.status_code != 200:
        return Response({"error": "User history not found"}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve order history for the user
    order_url = f"http://localhost:8000/order/history?user_id={user_id}"
    order_response = requests.get(order_url)
    if order_response.status_code != 200:
        return Response({"error": "Order history not found"}, status=status.HTTP_404_NOT_FOUND)

    # Combine and return user and order data
    user_data = user_response.json()
    order_data = order_response.json()
    combined_data = {"user": user_data, "orders": order_data}
    return Response(combined_data, status=status.HTTP_200_OK)
