from django.urls import path
from . import views

urlpatterns = [
    path('menu/<str:restaurant>/', views.get_menu, name='get_menu'),
    path('order/', views.place_order, name='place_order'),
    path('history/<str:user_id>/', views.get_user_order_history, name='get_user_order_history'),
]
