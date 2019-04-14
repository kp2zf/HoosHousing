from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.db.models import Q
from django.views.generic import FormView, TemplateView
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from django.views.generic.edit import UpdateView
from .forms import BuildingForm, BuildingImageForm, ReviewForm, UnitForm, UpdateForm
from .models import Building, Unit, Review, Vote

def home(request):
    buildings = Building.objects.all()
    return render(request,'home.html',{'buildings':buildings})

def review(request):
    buildings = Building.objects.all()
    return render(request,'review_buildings.html',{'buildings':buildings})

def building_detail(request, pk=None, sorting= '-date'):
	building = get_object_or_404(Building, pk=pk)
	reviews = building.review_set.all()
	reviews = reviews.order_by(sorting)
	return render(request,'building_detail.html',{'building':building, 'reviews':reviews, 'sorting':sorting})

class AddBuildingView(FormView):
	template_name = 'add_building.html'
	form_class = BuildingForm
	success_url = reverse_lazy('housing:success')
	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		print('add_form form valid')
		form.save(admin=self.request.user.username)
		return super().form_valid(form)

def upload_building_image(request, pk=None):
	building = get_object_or_404(Building, pk=pk)
	print('post', request.POST, 'files', request.FILES)
	form = BuildingImageForm(request.POST, request.FILES)
	if form.is_valid():
		print('form is valid!', form)
		form.save(building)
	return redirect('/')

class SearchView(TemplateView):
	template_name = 'search.html'
class AdvancedSearchView(TemplateView):
	template_name = 'advanced_search.html'
def search(request):
	template = 'results.html'

	search_query = request.GET.get('search_box')
	neighborhood_query = request.GET.get('neighborhood')
	bedroom_query = request.GET.get('bedrooms')
	if(neighborhood_query!=""):
		neighborhood_query=Q(neighborhood__icontains=neighborhood_query)
	else:
		neighborhood_query=Q(name__icontains=search_query)
	if(bedroom_query!=""):
		bedroom_query=Q(unit__num_bedrooms__icontains=bedroom_query)
	else:
		bedroom_query=Q(name__icontains=search_query)

	search_query=Q(name__icontains=search_query)
	buildings = Building.objects.filter(neighborhood_query&bedroom_query&search_query).distinct()
	return render(request, 'search.html',{'buildings':buildings, 'isSearchResult': True})

class SuccessView(TemplateView):
	template_name = 'building_success.html'

def advanced_search(request):
	template = 'results.html'

	search_query = request.GET.get('search_box')
	neighborhood_query = request.GET.get('neighborhood')
	bedroom_query = request.GET.get('bedrooms')

	search_query=Q(name__icontains=search_query)
	
	pet_query=request.GET.get('pet_allowed')
	if(pet_query=="True"):
		pet_query=Q(pet_allowed=True)
	elif(pet_query=="False"):
		pet_query=Q(pet_allowed=False)
	else:
		pet_query=search_query

	parking_query=request.GET.get('parking')
	if(parking_query=="True"):
		parking_query=Q(parking=True)
	elif(parking_query=="False"):
		parking_query=Q(parking=False)
	else:
		parking_query=search_query

	furnished_query=request.GET.get('furnished')
	if(furnished_query=="True"):
		furnished_query=Q(is_furnished=True)
	elif(furnished_query=="False"):
		furnished_query=Q(is_furnished=False)
	else:
		furnished_query=search_query

	air_condition_query=request.GET.get('air_condition')
	if(air_condition_query=="True"):
		air_condition_query=Q(air_conditioning=True)
	elif(furnished_query=="False"):
		air_condition_query=Q(air_conditioning=False)
	else:
		air_condition_query=search_query
	
	if(neighborhood_query!=""):
		neighborhood_query=Q(neighborhood__icontains=neighborhood_query)
	else:
		neighborhood_query=search_query
	if(bedroom_query!=""):
		bedroom_query=Q(unit__num_bedrooms__icontains=bedroom_query)
	else:
		bedroom_query=search_query

	
	buildings = Building.objects.filter(neighborhood_query&bedroom_query&search_query&pet_query&air_condition_query&furnished_query&parking_query).distinct()
	return render(request, 'advanced_search.html',{'buildings':buildings, 'isSearchResult': True})

class AddUnitView(TemplateView):
    template_name = 'add_unit.html'
    success_url = reverse_lazy('housing:add_unit')

    def get(self, request, pk=None):
        form = UnitForm()
        return render(request, 'add_unit.html', {'form': form})

    def post(self, request, pk=None):
        unit_form = UnitForm(request.POST)
        building = get_object_or_404(Building, pk=pk)
        if unit_form.is_valid():
            unit_form.save(building)
            return render(request,'building_detail.html',{'building':building })
        return render(request, 'add_unit.html', args)

def add_review(request, pk):
	building = get_object_or_404(Building, pk=pk)
	if request.method == 'POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			form.save(building)
			return redirect(reverse('housing:building_detail', kwargs={'pk': pk}))
	else:
		form = ReviewForm()
	return render(request, 'add_review.html', {'form': form})

def helpful_vote(request, pk, reviewer_name, voter_name, sorting= '-date'): #eventually change name to userid
	#need to add sorting so page refreshes to same sorting option that was selected before
	building = get_object_or_404(Building, pk=pk)
	review = Review.objects.get(building=building, name=reviewer_name)
	try:
		vote = Vote.objects.get(review=review, username=voter_name)
		vote.delete()
		review.helpful_score -= 1
		review.save()
		return redirect(reverse('housing:building_detail', kwargs={'pk':pk, 'sorting':sorting}))
	except ObjectDoesNotExist:
		vote = Vote(review=review, username=voter_name)
		vote.save()
		review.helpful_score += 1
		review.save()
		return redirect(reverse('housing:building_detail', kwargs={'pk':pk, 'sorting':sorting}))

def toggle_building_published(request, pk):
	building = get_object_or_404(Building, pk=pk)
	building.approved = not building.approved
	building.save()
	return redirect(reverse('housing:review'))

def update_building(request, pk):
	building = get_object_or_404(Building, pk=pk)
	if request.method == 'POST':
		form=UpdateForm(request.POST)
		if form.is_valid():
			building.address=form.cleaned_data['address']
			building.save()
	else:
		form=UpdateForm()
	return redirect(reverse('housing:building_detail', kwargs={'pk': pk}))

def myaccount(request):
	if request.user.is_authenticated:
		reviews = Review.objects.filter(Q(name=request.user.username))
		return render(request, 'myaccount.html', {'reviews':reviews})
	return render(request,'myaccount.html')

def my_logout(request):
    logout(request)
    return redirect(reverse('housing:index'))
class EditBuilding(UpdateView):
	template_name = 'edit.html'
	model=Building
	fields=['name','address']
	success_url = reverse_lazy('housing:index')
