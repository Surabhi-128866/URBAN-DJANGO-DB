
import os
import django
import sys

# Setup Django environment
sys.path.append('c:\\Users\\SURABHI\\OneDrive\\Desktop\\urban-django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urban_habitat.settings')
django.setup()

from analyzer.models import Habitat
from analyzer.utils import get_city_image

def fix_images_v2():
    print("Diversifying habitat images...")
    habitats = Habitat.objects.all()
    count = 0
    
    for habitat in habitats:
        print(f"Updating image for: {habitat.name}")
        # This will now use the new hashed logic to pick a different image for each name
        habitat.image_url = get_city_image(habitat.name)
        habitat.save()
        count += 1
        
    print(f"Successfully updated {count} habitats with DIVERSE images.")

if __name__ == "__main__":
    fix_images_v2()
