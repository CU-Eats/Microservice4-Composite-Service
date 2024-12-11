from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from asgiref.sync import async_to_sync
from Order.api.serializers import DummySerializer
import aiohttp
import asyncio
import uuid
from django.conf import settings


class OrderViewSet(viewsets.GenericViewSet):

    serializer_class = DummySerializer
    queryset = []
    @action(detail=False, methods=['POST'])
    def create_batch_order(self, request):
        message, status_code = self.check_food_exists(request)
        if status_code == -1:
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        return async_to_sync(self._create_batch_order)(request)

    async def _create_batch_order(self, request):
        ORDER_SERVICE_URL = f"{settings.ORDER_SERVICE_HOST}/api/orders/"

        user_id = request.data.get('user_id')
        user_name = request.data.get('user_name')
        products = request.data.get('products', [])

        if not user_id or not user_name:
            return Response(
                {'error': "The 'user_id' and 'user_name' fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not products:
            return Response(
                {'error': "The 'products' field is required and should contain a list of products."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order_id = uuid.uuid4().int >> 64

        created_orders = []
        errors = []

        async with aiohttp.ClientSession() as session:
            tasks = []
            for product in products:
                required_fields = ['product_name', 'restaurant_name', 'quantity']
                missing_fields = [field for field in required_fields if field not in product]
                if missing_fields:
                    errors.append(
                        {'product': product, 'error': f"Missing fields: {', '.join(missing_fields)}"}
                    )
                    continue

                product_payload = {
                    'order_id': order_id,
                    'product_name': product['product_name'],
                    'restaurant_name': product['restaurant_name'],
                    'quantity': product['quantity'],
                    'user_id': user_id,
                    'user_name': user_name
                }

                tasks.append(self._make_order_request(session, ORDER_SERVICE_URL, product, product_payload))

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, dict) and 'error' in result:
                    errors.append(result)
                else:
                    created_orders.append(result)

        response_data = {
            'order_id': order_id,
            'user_id': user_id,
            'user_name': user_name,
            'created_orders': created_orders,
            'errors': errors
        }

        if created_orders:
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def check_food_exists(self, request):
        products = request.data.get('products', [])
        if not products:
            return Response(
                {'error': "The 'products' field is required and should contain a list of products."},
                status=status.HTTP_400_BAD_REQUEST
            )
        for product in products:
            restaurant_name = product['restaurant_name']
            product_name = product['product_name']
            PRODUCT_SERVICE_URL = f"{settings.RESTAURANT_URL}/restaurant/getMenu/{restaurant_name}"
            try:
                response = requests.get(PRODUCT_SERVICE_URL)
                if response.status_code != 200:
                    return ("invalid restaurant", -1)
                else:
                    data = response.json()
                    restaurant_products = [p['name'] for p in data]
                    if product_name not in restaurant_products:
                        return ("invalid product", -1)

            except requests.RequestException as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return ("valid", 1)

    async def _make_order_request(self, session, url, product, payload):
        try:
            async with session.post(url, json=payload) as response:
                if response.status == 201:
                    return await response.json()
                else:
                    return {'product': product, 'error': await response.json()}
        except Exception as e:
            return {'product': product, 'error': str(e)}

    @action(detail=False, methods=['GET'])
    def user_orders(self, request):
        # Use async_to_sync to call an async method
        return async_to_sync(self._user_orders)(request)

    async def _user_orders(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'The "user_id" parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        ORDER_SERVICE_URL = f"{settings.ORDER_SERVICE_HOST}/api/orders/user_orders/"
        params = {'user_id': user_id}

        created_at = request.query_params.get('created_at')
        if created_at:
            params['created_at'] = created_at

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(ORDER_SERVICE_URL, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return Response(data, status=status.HTTP_200_OK)
                    else:
                        error_details = await response.json()
                        return Response(
                            {'error': f"Failed to fetch orders. Details: {error_details}"},
                            status=response.status
                        )
            except Exception as e:
                return Response(
                    {'error': f"An error occurred while fetching orders: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
