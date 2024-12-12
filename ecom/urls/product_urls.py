
from django.urls import path
from ecom.views import product_views as views


urlpatterns = [
	path('api/v1/product/all/', views.getAllProduct),

	path('api/v1/product/without_pagination/all/', views.getAllProductWithoutPagination),
    
	path('api/v1/product/latest_product/', views.getLatestProducts),

	path('api/v1/product/<int:pk>', views.getAProduct),

	path('api/v1/product/search/', views.searchProduct),

	path('api/v1/product/create/', views.createProduct),

	path('api/v1/roduct/update/<int:pk>', views.updateProduct),

	path('api/v1/product/delete/<int:pk>', views.deleteProduct),


]