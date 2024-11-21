from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions
from ecom.models import OrderItem
from ecom.serializers import OrderItemSerializer, OrderItemListSerializer
from ecom.filters import OrderItemFilter

from commons.enums import PermissionEnum
from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		
		OpenApiParameter("size"),
  ],
	request=OrderItemSerializer,
	responses=OrderItemSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllOrderItem(request):
	order_items = OrderItem.objects.all()
	total_elements = order_items.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	order_items = pagination.paginate_data(order_items)

	serializer = OrderItemListSerializer(order_items, many=True)

	response = {
		'order_items': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=OrderItemSerializer,
	responses=OrderItemSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllOrderItemWithoutPagination(request):
	order_items = OrderItem.objects.all()

	serializer = OrderItemListSerializer(order_items, many=True)

	return Response({'order_items': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=OrderItemSerializer, responses=OrderItemSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getAOrderItem(request, pk):
	try:
		city = OrderItem.objects.get(pk=pk)
		serializer = OrderItemSerializer(city)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"OrderItem id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=OrderItemSerializer, responses=OrderItemSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchOrderItem(request):
	order_items = OrderItemFilter(request.GET, queryset=OrderItem.objects.all())
	order_items = order_items.qs

	print('searched_order_items: ', order_items)

	total_elements = order_items.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	order_items = pagination.paginate_data(order_items)

	serializer = OrderItemListSerializer(order_items, many=True)

	response = {
		'order_items': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(order_items) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no order_items matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=OrderItemSerializer, responses=OrderItemSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createOrderItem(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value

	serializer = OrderItemSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=OrderItemSerializer, responses=OrderItemSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateOrderItem(request,pk):
	try:
		city = OrderItem.objects.get(pk=pk)
		data = request.data
		serializer = OrderItemSerializer(city, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"OrderItem id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=OrderItemSerializer, responses=OrderItemSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteOrderItem(request, pk):
	try:
		city = OrderItem.objects.get(pk=pk)
		city.delete()
		return Response({'detail': f'OrderItem id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"OrderItem id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

