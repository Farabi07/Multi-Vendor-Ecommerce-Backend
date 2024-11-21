
from django.urls import path
from ecom.views import orderItem_views as views


urlpatterns = [
	path('api/v1/orderItem/all/', views.getAllOrderItem),

	path('api/v1/orderItem/without_pagination/all/', views.getAllOrderItemWithoutPagination),

	path('api/v1/orderItem/<int:pk>', views.getAOrderItem),

	path('api/v1/orderItem/search/', views.searchOrderItem),

	path('api/v1/orderItem/create/', views.createOrderItem),

	path('api/v1/orderItem/update/<int:pk>', views.updateOrderItem),

	path('api/v1/orderItem/delete/<int:pk>', views.deleteOrderItem),


]