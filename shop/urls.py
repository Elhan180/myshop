from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('order/create/', views.order_create, name='order_create'),
    path('profile/', views.profile, name='profile'),
    path('order/payment/<int:order_id>/', views.order_payment, name='order_payment'),
    path('main/', views.index, name='index'),
    path('', views.product_list, name='product_list'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('profile/clear/', views.clear_order_history, name='clear_order_history'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('category/<slug:category_slug>/', views.product_list, name='category_products'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    

]
