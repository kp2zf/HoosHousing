from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q

from .forms import BuildingForm
from .models import Building

def home(request):
    buildings = Building.objects.all()
    return render(request,'home.html',{'buildings':buildings})

def building_detail(request, pk=None):
	building = get_object_or_404(Building, pk=pk)
	return render(request,'building_detail.html',{'building':building})

class AddBuildingView(generic.FormView):
	template_name = 'add_building.html'
	form_class = BuildingForm
	success_url = reverse_lazy('housing:add_building')

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		print('add_form form valid')
		form.save_building()
		return super().form_valid(form)

def search(request):
	template = 'results.html'

	search_query=request.GET.get('search_box')
	neighborhood_query=request.GET.get('neighborhood')
	bedroom_query=request.GET.get('bedrooms')
	buildings=Building.objects.filter(Q(unit__num_bedrooms__icontains=bedroom_query)&Q(neighborhood__icontains=neighborhood_query)&Q(name__icontains=search_query)).distinct()

	return render(request, 'listing_page.html',{'buildings':buildings})
