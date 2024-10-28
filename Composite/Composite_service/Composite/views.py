import requests
import asyncio
import aiohttp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# 1. GET Menu with Query Parameters (Synchronous)
@api_view(['GET'])
def get_menu(request, restaurant):
    url = "http://localhost:8000/restaurant/everything"
    response = requests.get(url, params={"restaurant": restaurant})
    if response.status_code == 200:
        menu_items = [item for item in response.json() if item['restaurant'] == restaurant]
        return Response(menu_items, status=status.HTTP_200_OK)
    return Response({"error": "Could not retrieve menu"}, status=status.HTTP_400_BAD_REQUEST)

# 2. POST - Place Order (Synchronous Call to User and Menu Services)
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
    menu_url = "http://localhost:8000/restaurant/everything"
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

# 3. PUT - Update an Existing Order (Synchronous)
@api_view(['PUT'])
def update_order(request, order_id):
    update_url = f"http://localhost:8000/order/{order_id}/update"
    response = requests.put(update_url, json=request.data)
    if response.status_code == 200:
        return Response(response.json(), status=status.HTTP_200_OK)
    return Response({"error": "Order update failed"}, status=status.HTTP_400_BAD_REQUEST)

# 4. Asynchronous Call to Fetch Order and User History
async def fetch_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json() if response.status == 200 else None

@api_view(['GET'])
async def get_user_order_history(request, user_id):
    # Asynchronously fetch user and order history
    user_url = f"http://localhost:8000/user/{user_id}/history"
    order_url = f"http://localhost:8000/order/history?user_id={user_id}"

    # Fetch data concurrently
    user_data, order_data = await asyncio.gather(
        fetch_async(user_url),
        fetch_async(order_url)
    )

    if not user_data:
        return Response({"error": "User history not found"}, status=status.HTTP_404_NOT_FOUND)
    if not order_data:
        return Response({"error": "Order history not found"}, status=status.HTTP_404_NOT_FOUND)

    combined_data = {"user": user_data, "orders": order_data}
    return Response(combined_data, status=status.HTTP_200_OK)
