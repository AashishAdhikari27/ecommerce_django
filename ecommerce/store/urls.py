
from django.urls import path

from . import views



urlpatterns = [
    
	#Leave as empty string for base url

	path('', views.store, name="store"),

	path('cart/', views.cart, name="cart"),

	path('checkout/', views.checkout, name="checkout"),
    
	path('update_item/', views.updateItem, name="update_item"),
    
	path('process_order/', views.processOrder, name="process_order"),
	
	# path('esewa_payment_success/', views.esewa_payment_success, name="esewa_payment_success"),
  
    # path('esewa_payment_failure/', views.esewa_payment_failure, name="esewa_payment_failure"),
]



