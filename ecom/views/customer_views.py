from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions
from ecom.models import Customer
from ecom.serializers import CustomerSerializer, CustomerListSerializer
from ecom.filters import CustomerFilter

from commons.enums import PermissionEnum
from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		
		OpenApiParameter("size"),
  ],
	request=CustomerSerializer,
	responses=CustomerSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllCustomer(request):
	customers = Customer.objects.all()
	total_elements = customers.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	customers = pagination.paginate_data(customers)

	serializer = CustomerListSerializer(customers, many=True)

	response = {
		'customers': serializer.data,
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
	request=CustomerSerializer,
	responses=CustomerSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllCustomerWithoutPagination(request):
	customers = Customer.objects.all()

	serializer = CustomerListSerializer(customers, many=True)

	return Response({'customers': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=CustomerSerializer, responses=CustomerSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getACustomer(request, pk):
	try:
		city = Customer.objects.get(pk=pk)
		serializer = CustomerSerializer(city)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Customer id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CustomerSerializer, responses=CustomerSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchCustomer(request):
	customers = CustomerFilter(request.GET, queryset=Customer.objects.all())
	customers = customers.qs

	print('searched_customers: ', customers)

	total_elements = customers.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	customers = pagination.paginate_data(customers)

	serializer = CustomerListSerializer(customers, many=True)

	response = {
		'customers': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(customers) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no customers matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CustomerSerializer, responses=CustomerSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createCustomer(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value

	serializer = CustomerSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CustomerSerializer, responses=CustomerSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateCustomer(request,pk):
	try:
		city = Customer.objects.get(pk=pk)
		data = request.data
		serializer = CustomerSerializer(city, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"Customer id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CustomerSerializer, responses=CustomerSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteCustomer(request, pk):
	try:
		city = Customer.objects.get(pk=pk)
		city.delete()
		return Response({'detail': f'Customer id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Customer id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

