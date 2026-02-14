
import os
import django
import sys
import time

# Setup Django environment
sys.path.append('c:\\Users\\SURABHI\\OneDrive\\Desktop\\urban-django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urban_habitat.settings')
django.setup()

from analyzer.models import Habitat
from analyzer.utils import get_city_image

def fix_images_v3():
    print("Fetching authentic images from Wikipedia...")
    habitats = Habitat.objects.all()
    count = 0
    
    for habitat in habitats:
        print(f"Processing: {habitat.name}...")
        # Since I updated get_city_image to use Wiki, calling it here will fetch the REAL image
        new_image = get_city_image(habitat.name)
        
        if new_image and new_image != habitat.image_url:
            habitat.image_url = new_image
            habitat.save()
            print(f" -> Updated to real image: {new_image}")
        else:
            print(" -> No change or fetch failed.")
        
        count += 1
        time.sleep(1) # Be nice to Wiki API
        
    print(f"Finished processing {count} habitats.")

if __name__ == "__main__":
    fix_images_v3()
