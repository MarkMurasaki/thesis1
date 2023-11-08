from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
    path('store2/', views.store2, name="store2"),
    path('store3/', views.store3, name="store3"),
	path('cart/', views.cart, name="cart"),
    path('cart2/', views.cart2, name="cart2"),
    path('add/', views.add, name="add"),
    path('orders/', views.orders, name="orders"),
    path('checkout2/', views.checkout2, name="checkout2"),
	path('checkout/', views.checkout, name="checkout"),
    path('login/', views.login, name="login"),
    path('logoutuser/', views.logoutuser, name="logoutuser"),
    path('registration/', views.registration, name="registration"),
    path ('update/<int:pk>/', views.update, name = 'update'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('toggle/<int:pk>/', views.toggle_item, name='toggle_item'),
    path('inventory/', views.inventory, name="inventory"),

	path('update_item/', views.updateItem, name="update_item"),
    path('update_item2/', views.updateItem2, name="update_item2"),
	path('process_order/', views.processOrder, name="process_order"),

]