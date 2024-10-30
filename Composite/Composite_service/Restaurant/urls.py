from django.urls import path
from . import views

urlpatterns = [
    path('getMenu/<str:restaurant_name>/', views.call_get_food_items_by_restaurant, name='get_menu'),
    path('add/', views.call_add_food_item, name='add'),
]
