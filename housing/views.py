from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.shortcuts import render

from .forms import BuildingForm, UnitForm
from .models import Building, Unit

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

class AddUnitView(TemplateView):
    template_name = 'add_unit.html'
    # form_class = UnitForm
    success_url = reverse_lazy('housing:add_unit')

    # def form_valid(self, form):
    #     print('add_form form valid')
    #     form.save_unit()
    #     return super().form_valid(form)

    def get(self, request):
        form = UnitForm()
        # building = get_object_or_404(Building)
        buildings = Building.objects.all()
        args = {'form': form, 'building': buildings}
        return render(request, 'add_unit.html', {'form': form})

    def post(self, request):
        form = UnitForm(request.POST)
        if form.is_valid():
            unit.building = request.building
            monthly_rent = form.cleaned_data['monthly_rent']
            square_footage = form.cleaned_data['square_footage']
            num_bedrooms = form.cleaned_data['num_bedrooms']
            available = form.cleaned_data['available']
            Unit(monthly_rent=monthly_rent, square_footage=square_footage, num_bedrooms=num_bedrooms, available=available).save()


        args = {'form': form, 'monthly_rent': monthly_rent, 'square_footage': square_footage, 'num_bedrooms': num_bedrooms, 'available': available}
        return render(request, 'add_unit.html', args)
