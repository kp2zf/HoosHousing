from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from .forms import BuildingForm
from .models import Building

def home(request):
    buildings = Building.objects.all()
    return render(request,'home.html',{'buildings':buildings})

def building_detail(request, pk=None):
	building = get_object_or_404(Building, pk=pk)
	return render(request,'building_detail.html',{'building':building})

def login(request):
	return render(request, 'login.html')

def logout(request):
	return render(request, 'login.html')


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