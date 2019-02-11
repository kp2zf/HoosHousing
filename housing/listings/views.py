from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from .models import Listing

def home(request):
    listings = Listing.objects.all()

    return render(request,'home.html',{'listings':listings})


def listing_detail(request,id):
    try:
        listing = Listing.objects.get(id=id)
    except Listing.DoesNotExist:
        raise Http404('listing not found')
    return render(request,'listing_detail.html',{'listing':listing})