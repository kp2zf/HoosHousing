from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from .models import Building

def home(request):
    buildings = Building.objects.all()

    return render(request,'home.html',{'buildings':buildings})


def building_detail(request,id):
    try:
        building = Building.objects.get(id=id)
    except Building.DoesNotExist:
        raise Http404('building not found')
    return render(request,'building_detail.html',{'building':building})