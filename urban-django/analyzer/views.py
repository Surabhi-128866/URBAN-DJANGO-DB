from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Habitat
from .utils import get_habitat_data

@login_required
def index(request):
    habitats = [] # History or featured
    searched_habitat = None
    
    if request.method == 'POST':
        location = request.POST.get('location')
        if location:
            # Check if button clicked was search
            data = get_habitat_data(location)
            print(f"DEBUG: Data returned for {location}: {data}") # DEBUG
            if data:
                if 'error' in data:
                    print("DEBUG: Error found in data, rendering error page") # DEBUG
                    # Location not found case
                    # Fetch recent habitats so page isn't empty
                    recent_habitats = Habitat.objects.filter(user=request.user).order_by('-id')[:6]
                    return render(request, 'analyzer/index.html', {
                        'habitats': recent_habitats, 
                        'error_message': data['error'],
                        'suggestions': data.get('suggestions', []),
                        'current_filter': '',
                        'searched_habitat': None
                    })
                
                # Save or update cache
                description = data['description']
                warning = data.get('warning')
                
                # Prepend warning to description for persistence
                if warning:
                    description = f"NOTE: {warning}\n\n{description}"

                obj, created = Habitat.objects.update_or_create(
                    name__iexact=location,
                    user=request.user, # ISOLATION: Only look for THIS user's record
                    defaults={
                        'name': location.title(),
                        'population_density': data['population_density'],
                        'crime_rate': data['crime_rate'],
                        'green_space': data['green_space'],
                        'schools': data['schools'],
                        'hospitals': data['hospitals'],
                        'restaurants': data['restaurants'],
                        'malls': data['malls'],
                        'description': description,
                        'image_url': data['image_url'],
                        'latitude': data['latitude'],
                        'longitude': data['longitude'],
                        'pollution_level': data['pollution_level']
                    }
                )
                searched_habitat = obj
    
    # Get Filter Parameter
    filter_type = request.GET.get('filter', '')
    
    # Base Query: ISOLATION -> Only show habitats for this user
    habitats = Habitat.objects.filter(user=request.user)
    
    # Apply Filters
    if filter_type == 'best':
        # Best = High Green Space + Low Crime (Simplified sorting)
        habitats = habitats.order_by('-green_space', 'crime_rate')[:6]
    elif filter_type == 'polluted':
        habitats = habitats.order_by('-pollution_level')[:6]
    elif filter_type == 'green':
        habitats = habitats.order_by('-green_space')[:6]
    else:
        # Default: History or Featured
        habitats = habitats.order_by('-id')[:6]

    return render(request, 'analyzer/index.html', {
        'habitats': habitats, 
        'searched_habitat': searched_habitat,
        'current_filter': filter_type,
        'warning_message': locals().get('warning') # Pass warning if it exists in local scope
    })

@login_required
def habitat_details(request, habitat_id):
    habitat = Habitat.objects.get(id=habitat_id)
    
    # Generate recommendations on the fly (or store them if needed, but on-fly is fine)
    # We need to construct a dict properly, or just pass the model object if helper handles it.
    # The helper expects a dict. Let's convert model to dict or adjust helper.
    # Easier: adjust helper or just pass the values.
    # Let's simple pass a dict.
    data = {
        'green_space': habitat.green_space,
        'crime_rate': habitat.crime_rate,
        'population_density': habitat.population_density,
        'pollution_level': habitat.pollution_level,
        'malls': habitat.malls
    }
    
    from .utils import get_recommendations, get_nearby_amenities
    recommendations = get_recommendations(data)
    
    # Fetch amenities for the details page (Preview)
    amenities = get_nearby_amenities(habitat.latitude, habitat.longitude)
    
    return render(request, 'analyzer/details.html', {
        'habitat': habitat,
        'recommendations': recommendations,
        'amenities': amenities
    })

@login_required
def amenities_view(request, habitat_id):
    habitat = Habitat.objects.get(id=habitat_id)
    
    # Fetch amenities for the dedicated page
    from .utils import get_nearby_amenities
    amenities = get_nearby_amenities(habitat.latitude, habitat.longitude)
    
    return render(request, 'analyzer/amenities.html', {
        'habitat': habitat,
        'amenities': amenities
    })

@login_required
def compare(request):
    habitats = Habitat.objects.all()
    return render(request, 'analyzer/compare_setup.html', {'habitats': habitats})

@login_required
def compare_result(request):
    h1_id = request.GET.get('h1')
    h2_id = request.GET.get('h2')
    
    if h1_id and h2_id:
        h1 = Habitat.objects.get(id=h1_id)
        h2 = Habitat.objects.get(id=h2_id)
        return render(request, 'analyzer/compare_result.html', {'h1': h1, 'h2': h2})
    
    return redirect('compare')

def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'analyzer/register.html', {'form': form})

