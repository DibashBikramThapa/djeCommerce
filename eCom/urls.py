from django.urls import path
from eCom.views import (HomeView,ItemDetailView,OrderItemDeleteView,
                        Checkout,add_to_cart,remove_from_cart,
                        OrderSummaryView, remove_single_item_from_cart,
                        PaymentView,ShirtView,ShirtWearView,OutWearView)

app_name='eCom'

urlpatterns=[
    path('',HomeView.as_view(),name='Home'),
    path('shirt/',ShirtView.as_view(),name='s'),
    path('shirtwear/',ShirtWearView.as_view(),name='sw'),
    path('outwear/',OutWearView.as_view(),name='ow'),
    path('order-summary/',OrderSummaryView.as_view(),name='order_summary'),
    path('checkout/',Checkout.as_view(),name='checkout'),
    path('products/<int:pk>/',ItemDetailView.as_view(),name='productpage'),
    path('add_to_cart/<int:pk>/',add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:pk>/',remove_from_cart,name='remove_from_cart'),
    path('remove_single_item_from_cart/<int:pk>/',remove_single_item_from_cart,name='remove_single_item_from_cart'),
    path('delete/<int:pk>/',OrderItemDeleteView,name='deleteoi'),
    path('payment/<payment_option>/',PaymentView.as_view(),name='payment'),
    #path('list/<category>/',CategoryView.as_view(),name='Category')
]
