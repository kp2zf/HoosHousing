from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.db.models import Q
from django.utils import timezone
from django.views.generic import FormView, TemplateView
from django.shortcuts import render

from .forms import BuildingForm, BuildingImageForm, ReviewForm, UnitForm
from .models import Building, Unit

def home(request):
    buildings = Building.objects.all()
    return render(request,'home.html',{'buildings':buildings})

def building_detail(request, pk=None):
	building = get_object_or_404(Building, pk=pk)
	return render(request,'building_detail.html',{'building':building})

class AddBuildingView(FormView):
	template_name = 'add_building.html'
	form_class = BuildingForm
	success_url = reverse_lazy('housing:add_building')

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		print('add_form form valid')
		form.save_building()
		return super().form_valid(form)

def upload_building_image(request, pk=None):
	building = get_object_or_404(Building, pk=pk)
	print('post', request.POST, 'files', request.FILES)
	form = BuildingImageForm(request.POST, request.FILES)
	if form.is_valid(): 
		print('form is valid!', form)
		form.save_building(building) 
	return redirect('/') 

class SearchView(TemplateView):
	template_name = 'search.html'

def search(request):
	template = 'results.html'
	search_query = request.GET.get('search_box')
	neighborhood_query = request.GET.get('neighborhood')
	bedroom_query = request.GET.get('bedrooms')
	buildings = Building.objects.filter(Q(unit__num_bedrooms__icontains=bedroom_query)&Q(neighborhood__icontains=neighborhood_query)&Q(name__icontains=search_query)).distinct()
	print('got buildings:', buildings)
	return render(request, 'search.html',{'buildings':buildings, 'isSearchResult': True})

class AddUnitView(TemplateView):
    template_name = 'add_unit.html'
    success_url = reverse_lazy('housing:add_unit')

    def get(self, request, pk=None):
        form = UnitForm()
        return render(request, 'add_unit.html', {'form': form})

    def post(self, request, pk=None):
        form = UnitForm(request.POST)
        building = get_object_or_404(Building, pk=pk)
        if form.is_valid():
            form.save_unit(building)
            return render(request,'building_detail.html',{'building':building })
        return render(request, 'add_unit.html', args)

def add_review(request, pk):
	building = get_object_or_404(Building, pk=pk)
	if request.method == 'POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			review = form.save(commit=False)
			review.building = building
			review.date = timezone.now()
			review.save()
			return redirect(reverse('housing:building_detail', kwargs={'pk': pk}))
	else:
		form = ReviewForm()
	return render(request, 'add_review.html', {'form': form})
