from django_filters import rest_framework as filters

from ecom.models import *



#Blog
class ProductFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['title', ]

class ProductCategoryFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = ProductCategory
        fields = ['title', ]

class CustomerFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = ['title', ]

class OrderFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ['title', ]


class OrderItemFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = OrderItem
        fields = ['title', ]