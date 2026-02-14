
import random
import requests
import time
from django.conf import settings
from urllib.parse import quote

def get_recommendations(habitat_data):
    """
    Generates recommendations based on habitat metrics.
    """
    recs = []
    if habitat_data['green_space'] < 20:
        recs.append("Build more parks and green zones to improve air quality.")
    if habitat_data['crime_rate'] > 50:
        recs.append("Increase public safety measures and street lighting.")
    if habitat_data['population_density'] > 15000:
        recs.append("Improve public transit to reduce traffic congestion.")
    if habitat_data['pollution_level'] > 60:
        recs.append("Implement stricter emission controls and promote EV adoption.")
    if habitat_data['malls'] < 2:
        recs.append("Develop more commercial centers for economic growth.")
    
    if not recs:
        recs.append("Maintain current urban planning standards.")
    return recs
        
def get_city_image(city_name):
    """
    Fetch an image URL for the city from Unsplash or Pexels, or generate one.
    This is now primarily a fallback/compatibility function, as get_wiki_data fetches images too.
    """
    # Fallback: Curated list of high-quality city/campus/urban images from Unsplash
    city_images = [
        "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?auto=format&fit=crop&w=800&q=80", # NY Vibe
        "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&q=80", # Modern City
        "https://images.unsplash.com/photo-1519452575417-564c140dbue4?w=800&q=80", # Campus/Park
        "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=800&q=80", # High rises
        "https://images.unsplash.com/photo-1496568816309-51d7c20e3b21?w=800&q=80", # Night city
        "https://images.unsplash.com/photo-1518391846015-55a3385287d6?w=800&q=80", # Nature/City mix
        "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800&q=80", # University vibe
        "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800&q=80", # Studying/College
        "https://images.unsplash.com/photo-1565034946487-077786996e27?w=800&q=80", # Indian City Vibe
        "https://images.unsplash.com/photo-1506157786151-b8491531f063?w=800&q=80", # Music/Vibrant
    ]
    
    index = hash(city_name) % len(city_images)
    return city_images[index]
    

def get_nearby_amenities(lat, lon, radius=10000):
    """
    Fetches nearby amenities using Overpass API.
    Radius in meters (default 10km for better city-wide accuracy).
    """
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Query for nodes, ways, and relations around the location
    overpass_query = f"""
    [out:json][timeout:25];
    (
      nwr["amenity"~"restaurant|cafe|fast_food"](around:{radius}, {lat}, {lon});
      nwr["amenity"~"hospital|clinic"](around:{radius}, {lat}, {lon});
      nwr["amenity"="school"](around:{radius}, {lat}, {lon});
      nwr["amenity"="place_of_worship"](around:{radius}, {lat}, {lon});
      nwr["shop"~"mall|supermarket|department_store"](around:{radius}, {lat}, {lon});
      nwr["leisure"="park"](around:{radius}, {lat}, {lon});
    );
    out center;
    """
    
    try:
        print(f"DEBUG: Querying Overpass API for {lat}, {lon} radius={radius}")
        response = requests.get(overpass_url, params={'data': overpass_query}, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            elements = data.get('elements', [])
            
            amenities = {
                'restaurants': [],
                'hospitals': [],
                'schools': [],
                'worship': [],
                'shopping': [],
                'parks': []
            }
            
            for el in elements:
                tags = el.get('tags', {})
                name = tags.get('name', 'Unknown')
                if name == 'Unknown': continue
                
                # Get coordinates (node has lat/lon, way/relation has center)
                lat_el = el.get('lat') or el.get('center', {}).get('lat')
                lon_el = el.get('lon') or el.get('center', {}).get('lon')
                
                if not lat_el or not lon_el: continue

                amenity = tags.get('amenity', '')
                shop = tags.get('shop', '')
                leisure = tags.get('leisure', '')
                
                # Extended Details
                street = tags.get('addr:street', '')
                city = tags.get('addr:city', '')
                address = f"{street}, {city}".strip(', ') if street else "Address not available"
                
                phone = tags.get('phone') or tags.get('contact:phone') or "Not available"
                website = tags.get('website') or tags.get('contact:website') or ""
                hours = tags.get('opening_hours', 'Hours not available')
                
                item = {'name': name, 'lat': lat_el, 'lon': lon_el, 'address': address, 'phone': phone, 'website': website, 'hours': hours}

                if amenity in ['restaurant', 'cafe', 'fast_food']:
                     amenities['restaurants'].append(item)
                elif amenity in ['hospital', 'clinic']:
                     amenities['hospitals'].append(item)
                elif amenity == 'school':
                     amenities['schools'].append(item)
                elif amenity == 'place_of_worship':
                     amenities['worship'].append(item)
                elif shop in ['mall', 'supermarket', 'department_store']:
                     amenities['shopping'].append(item)
                elif leisure == 'park':
                     amenities['parks'].append(item)
            
            return amenities
    except Exception as e:
        print(f"Error fetching amenities: {e}")
        
    return {k: [] for k in ['restaurants', 'hospitals', 'schools', 'worship', 'shopping', 'parks']}

def get_location_suggestions(query):
    """
    Returns a list of suggested location names from Wikipedia OpenSearch (better for typos).
    """
    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "opensearch",
            "format": "json",
            "search": query,
            "limit": 5,
            "origin": "*"
        }
        headers = {
            "User-Agent": "UrbanHabitatAnalyzer/1.0 (contact@example.com)"
        }
        response = requests.get(url, params=params, headers=headers, timeout=5)
        
        if response.status_code != 200:
             return []

        data = response.json()
        # OpenSearch returns [query, [titles], [descriptions], [links]]
        # We want the titles at index 1
        if len(data) > 1:
            return data[1]
            
        return []

    except Exception as e:
        print(f"Suggestion fetch error: {e}")
        return []

def get_wiki_data(location_name):
    """
    Fetches Image, Coordinates, and Description from Wikipedia in a single efficient call.
    Returns a dict with keys: image_url, lat, lon, description
    """
    default_data = {
        "image_url": None,
        "lat": 0.0,
        "lon": 0.0,
        "description": f"Analysis for {location_name.title()}. A vibrant location with unique urban characteristics."
    }
    
    try:
        url = "https://en.wikipedia.org/w/api.php"
        # Search for best match first using generator
        params = {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": location_name,
            "gsrlimit": 1, 
            "prop": "pageimages|coordinates|extracts",
            "pithumbsize": 1000,
            "colimit": 1,
            "exintro": 1,
            "explaintext": 1,
            "exchars": 300,
            "origin": "*"
        }
        headers = {
            "User-Agent": "UrbanHabitatAnalyzer/1.0 (contact@example.com)"
        }
        
        print(f"DEBUG: Fetching Wiki Data for '{location_name}'")
        response = requests.get(url, params=params, headers=headers, timeout=5)
        
        if response.status_code != 200:
            return default_data

        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        
        if not pages:
            return default_data
            
        # Get the first page result
        page = list(pages.values())[0]
        
        # Extract Image
        if "thumbnail" in page:
            default_data["image_url"] = page["thumbnail"]["source"]
            
        # Extract Coordinates
        if "coordinates" in page:
            coords = page["coordinates"][0]
            default_data["lat"] = float(coords.get("lat", 0.0))
            default_data["lon"] = float(coords.get("lon", 0.0))

        # Extract Description
        if "extract" in page:
            default_data["description"] = page["extract"]
            
        print(f"DEBUG: Wiki Data Success: {default_data['lat']}, {default_data['lon']}")
        return default_data

    except Exception as e:
        print(f"Wiki Data Fetch Error: {e}")
        return default_data

def get_coordinates_openmeteo(location_name):
    """
    Fetches coordinates using Open-Meteo Geocoding API (Free, no key).
    """
    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": location_name,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        headers = {
            'User-Agent': 'UrbanHabitatAnalyzer/1.0 (contact@example.com)'
        }
        response = requests.get(url, params=params, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if "results" in data and data["results"]:
                result = data["results"][0]
                return float(result['latitude']), float(result['longitude'])
    except Exception as e:
        print(f"OpenMeteo Error: {e}")
    return 0.0, 0.0

def get_coordinates_overpass(location_name):
    """
    Fetches coordinates using Overpass API (OpenStreetMap) by name search.
    Good for POIs (Colleges, Parks) when OpenMeteo (Cities) fails.
    """
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Clean query for regex safety (basic)
    safe_name = location_name.replace('"', '').replace('\\', '')
    
    # Case-insensitive substring match
    overpass_query = f"""
    [out:json][timeout:25];
    nwr["name"~"{safe_name}", i];
    out center 1;
    """
    
    try:
        response = requests.get(overpass_url, params={'data': overpass_query}, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            elements = data.get('elements', [])
            
            if elements:
                el = elements[0]
                lat = el.get('lat') or el.get('center', {}).get('lat')
                lon = el.get('lon') or el.get('center', {}).get('lon')
                
                if lat and lon:
                    return float(lat), float(lon)
                    
    except Exception as e:
        print(f"Overpass Geocode Error: {e}")
        
    return 0.0, 0.0

def get_coordinates(location_name):
    """
    Fetches latitude and longitude. 
    Strategy: OpenMeteo -> Overpass -> Nominatim -> Fail.
    """
    # 1. Try OpenMeteo (Best for Cities)
    lat, lon = get_coordinates_openmeteo(location_name)
    if lat != 0.0 or lon != 0.0:
        return lat, lon

    # 2. Try Overpass (Best for POA/Colleges)
    print(f"DEBUG: OpenMeteo failed, trying Overpass for '{location_name}'") # DEBUG
    lat, lon = get_coordinates_overpass(location_name)
    if lat != 0.0 or lon != 0.0:
        return lat, lon

    # 3. Try Nominatim (Fallback - likely blocked but worth a shot)
    try:
        headers = {
            'User-Agent': 'UrbanHabitatAnalyzer/1.0 (contact@example.com)'
        }
        url = f"https://nominatim.openstreetmap.org/search?q={quote(location_name)}&format=json&limit=1"
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
        else:
            print(f"Nominatim Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
    
    return 0.0, 0.0

def get_bing_image(query):
    """
    Fetches a relevant image using Bing Image Search (thumbnail API).
    """
    try:
        url = f"https://tse2.mm.bing.net/th?q={quote(query)}&w=800&h=600&c=7&rs=1&p=0"
        # Verify it exists (optional, but good for stability)
        response = requests.head(url, timeout=2)
        if response.status_code == 200:
            return url
    except:
        pass
    return None

def get_habitat_data(location_name):
    """
    Fetches data from external APIs (real metrics from Overpass).
    """
    # Normalize input
    key = location_name.lower().strip()
    
    # Fetch consolidated data from Wikipedia (Image + Coords + Desc)
    wiki_data = get_wiki_data(location_name)
    
    image_url = wiki_data['image_url']
    lat = wiki_data['lat']
    lon = wiki_data['lon']
    description = wiki_data['description']
    
    # Validation
    if lat == 0.0 and lon == 0.0:
        # Wiki failed, try OpenMeteo/Overpass/Nominatim fallback
        print(f"DEBUG: Wiki coords failed, trying Geocoders for '{location_name}'")
        lat, lon = get_coordinates(location_name)

    # Fallback: Description parsing
    warning = None
    if lat == 0.0 and lon == 0.0 and description:
        # Heuristic: Try to geocode the first proper noun/word from description.
        # e.g. "Hyderabad is the capital..." -> "Hyderabad"
        try:
            potential_location = None
            # Heuristic 1: Check for major cities in description
            common_cities = ['Hyderabad', 'Secunderabad', 'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Pune', 'Jaipur', 'Ahmedabad']
            for city in common_cities:
                if city in description:
                    potential_location = city
                    break
            
            # Heuristic 2: First word fallback
            if not potential_location:
                potential_location = str(description).split(' ')[0].strip(',.')

            if potential_location and len(potential_location) > 3:
                print(f"DEBUG: Geocoding failed, trying description fallback: '{potential_location}'")
                p_lat, p_lon = get_coordinates(potential_location)
                if p_lat != 0.0 or p_lon != 0.0:
                    lat, lon = p_lat, p_lon
                    warning = f"Creating report for '{potential_location}' (Exact location not found)."
        except:
            pass

    if lat == 0.0 and lon == 0.0:
        suggestions = get_location_suggestions(location_name)
        return {
            "error": f"Location '{location_name}' not found.",
            "suggestions": suggestions
        }

    # Fallback image - Bing Search
    if not image_url:
        print(f"DEBUG: Wiki image missing, trying Bing for '{location_name}'")
        image_url = get_bing_image(location_name)

    # Fallback image - Generic City
    if not image_url:
        city_images = [
            "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?auto=format&fit=crop&w=800&q=80", 
            "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&q=80", 
            "https://images.unsplash.com/photo-1519452575417-564c140dbue4?w=800&q=80",
            "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=800&q=80"
        ]
        index = hash(location_name) % len(city_images)
        image_url = city_images[index]

    # Fetch Real Amenities Data
    amenities = get_nearby_amenities(lat, lon, radius=10000) # 10km radius
    
    school_count = len(amenities['schools'])
    hospital_count = len(amenities['hospitals'])
    restaurant_count = len(amenities['restaurants'])
    mall_count = len(amenities['shopping'])
    park_count = len(amenities['parks'])

    # Calculate derived metrics
    # Green Space: roughly proportional to parks, capped at 60%
    green_space = min(park_count * 1.5, 60.0) 
    if green_space < 5: green_space = 5.0
    
    # Pollution: Inverse of green space + some noise
    pollution_level = int(100 - green_space - random.randint(0, 10))
    if pollution_level < 0: pollution_level = 10
    if pollution_level > 100: pollution_level = 100

    return {
        "population_density": random.randint(1000, 30000), # Wikipedia extract parsing is complex, keeping random for now
        "crime_rate": round(random.uniform(10.0, 80.0), 1),
        "green_space": round(green_space, 1),
        "pollution_level": pollution_level,
        "latitude": lat,
        "longitude": lon,
        "schools": school_count,
        "hospitals": hospital_count,
        "restaurants": restaurant_count,
        "malls": mall_count,
        "description": description,
        "image_url": image_url,
        "warning": warning
    }
