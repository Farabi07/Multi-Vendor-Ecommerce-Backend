from django.http import HttpResponse

def index(request):
	return HttpResponse("Welcome to Our Multi_Vendor Ecomerece site")