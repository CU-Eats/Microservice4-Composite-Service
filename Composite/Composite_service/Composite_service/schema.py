import graphene
from graphene_django.types import DjangoObjectType
from django.conf import settings
import requests

class RestaurantType(graphene.ObjectType):
    name = graphene.String()
    menu = graphene.List(graphene.String)

class OrderType(graphene.ObjectType):
    order_id = graphene.String()
    status = graphene.String()

class Query(graphene.ObjectType):
    restaurant_details = graphene.Field(
        RestaurantType,
        restaurant_name=graphene.String(required=True)
    )
    order_status = graphene.Field(
        OrderType,
        order_id=graphene.String(required=True)
    )

    def resolve_restaurant_details(self, info, restaurant_name):
        try:
            endpoint = f"{settings.RESTAURANT_URL}/restaurant/getMenu/{restaurant_name}/"
            response = requests.get(endpoint, timeout=10)
            if response.status_code == 200:
                menu_items = response.json()
                return RestaurantType(name=restaurant_name, menu=menu_items)
            else:
                return None
        except requests.exceptions.RequestException:
            return None

    def resolve_order_status(self, info, order_id):
        try:
            endpoint = f"{settings.RESTAURANT_URL}/api/orders/{order_id}/status/"
            response = requests.get(endpoint, timeout=10)
            if response.status_code == 200:
                status = response.json().get("status")
                return OrderType(order_id=order_id, status=status)
            else:
                return None
        except requests.exceptions.RequestException:
            return None

schema = graphene.Schema(query=Query)
