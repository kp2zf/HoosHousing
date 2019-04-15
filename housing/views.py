from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic

from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from django.db.models import Q
from django.views.generic import FormView, TemplateView

from django.views.generic.edit import UpdateView

from .forms import BuildingForm, BuildingImageForm, ReviewForm, UnitForm
from .models import Building, Unit, Review, Vote

def home(request):
	buildings = Building.objects.all()
	return render(request,'home.html',{'buildings':buildings})

def review(request):
	if request.user.is_superuser:
		buildings = Building.objects.all()
		return render(request,'review_buildings.html',{'buildings':buildings})
	else:
		return render(request, 'permission_error.html')

def building_detail(request, pk=None, sorting= '-date'):
	building = get_object_or_404(Building, pk=pk)
	reviews = building.review_set.all()
	reviews = reviews.order_by(sorting)
	rating_sum = 0
	rating_count = 0
	upvoted_reviews = [] # the reviews that have already been upvoted by this user
	for review in reviews:
		rating_sum += review.rating
		rating_count += 1
		votes = review.vote_set.all()
		voted_users = [vote.username for vote in votes]
		if request.user.username in voted_users:
			upvoted_reviews.append(review)
	if rating_count > 0:
		building.rating = rating_sum / rating_count
		building.rating = round(building.rating * 2.0) / 2.0
	return render(request, 'building_detail.html', {
		'building':building,
		'reviews':reviews,
		'upvoted_reviews': upvoted_reviews,
		'sorting':sorting
		})

class AddBuildingView(FormView):
	template_name = 'add_building.html'
	form_class = BuildingForm
	success_url = reverse_lazy('housing:success')
	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		form.save(self.request.user.username)
		return super().form_valid(form)

def upload_building_image(request, pk=None):
	building = get_object_or_404(Building, pk=pk)
	form = BuildingImageForm(request.POST, request.FILES)
	if form.is_valid():
		print('form is valid!', form)
		form.save(building)
	return redirect(reverse('housing:building_detail', kwargs={'pk': building.id}))

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
	elif(air_condition_query=="False"):
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
	return render(request, 'advanced_search.html', {'buildings':buildings, 'isSearchResult': True})

class AddUnitView(TemplateView):
	template_name = 'add_unit.html'
	success_url = reverse_lazy('housing:add_unit')

	def get(self, request, pk=None):
		building = get_object_or_404(Building, pk=pk)
		if request.user.username == building.admin:
			form = UnitForm()
			return render(request, 'add_unit.html', {'form': form})
		else:
			return render(request, 'permission_error.html')

	def post(self, request, pk=None):
		building = get_object_or_404(Building, pk=pk)
		if request.user.username == building.admin:
			unit_form = UnitForm(request.POST)
			if unit_form.is_valid():
				unit_form.save(building)
				return redirect(reverse('housing:building_detail',kwargs={'pk':pk}))
		else:
			return render(request, 'permission_error.html')
		return render(request, 'add_unit.html', args)

def add_review(request, pk):
	building = get_object_or_404(Building, pk=pk)
	if request.method == 'POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			form.save(building, request.user.username)
			return redirect(reverse('housing:building_detail', kwargs={'pk': pk}))
	else:
		form = ReviewForm()
	return render(request, 'add_review.html', {'form': form})

def EditReview(request, pk):
	building = get_object_or_404(Building, pk=pk)
	reviews = building.review_set.all()


def helpful_vote(request, pk, reviewer_name, voter_name, sorting= '-date'): #eventually change name to userid
	#need to add sorting so page refreshes to same sorting option that was selected before
	building = get_object_or_404(Building, pk=pk)
	review = Review.objects.get(building=building, name=reviewer_name)
	if not request.user.is_authenticated:
		return render(request, 'login.html')
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
	if request.user.is_superuser:
		building = get_object_or_404(Building, pk=pk)
		building.approved = not building.approved
		building.save()
		return redirect(reverse('housing:review'))
	else:
		return render(request, 'permission_error.html')

def myFavorites(request):
	if request.user.is_authenticated:
		buildings = Building.objects.all()
		return render(request, 'myFavorites.html', {'buildings': buildings})
	return render(request, 'myFavorites.html')

def myReviews(request):
	if request.user.is_authenticated:
		reviews = Review.objects.filter(Q(name=request.user.username))
		return render(request, 'myReviews.html', {'reviews': reviews})
	return render(request, 'myReviews.html')

def my_logout(request):
	logout(request)
	return redirect(reverse('housing:index'))

class EditBuilding(UpdateView):
	template_name = 'edit.html'
	model = Building
	fields = ['name','address','pet_allowed','is_furnished','air_conditioning','lease_length',
			'parking','pool','gym','neighborhood','website_link','email','phone_number']
	success_url = reverse_lazy('housing:index')

def favoriteBuilding(request, pk):
	url = request.META.get('HTTP_REFERER')

	b = get_object_or_404(Building, pk=pk)
	if request.user in b.favorites.all():
		b.favorites.remove(request.user)
	else:
		b.favorites.add(request.user)

	return HttpResponseRedirect(url)