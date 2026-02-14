
from analyzer.utils import get_nearby_amenities, get_coordinates

def test():
    city = "Hyderabad"
    print(f"Fetching coordinates for {city}...")
    lat, lon = get_coordinates(city)
    print(f"Coordinates: {lat}, {lon}")
    
    if lat == 0 and lon == 0:
        print("Failed to get coordinates.")
        return

    print("Fetching amenities...")
    amenities = get_nearby_amenities(lat, lon)
    
    # Need to modify utils temporarily or update this script to inline the request to see raw response.
    # Actually, let's just update utils.py to print the error if any, or print the count.
    # Better yet, let's update utils.py to have better error handling/logging.

    
    print("\nResults:")
    for category, items in amenities.items():
        print(f"\n--- {category} ---")
        for item in items:
            print(f"- {item['name']}")

if __name__ == "__main__":
    import os
    import django
    import sys
    
    # Setup Django environment
    sys.path.append('c:\\Users\\SURABHI\\OneDrive\\Desktop\\urban-django')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urban_habitat.settings')
    django.setup()
    
    test()
