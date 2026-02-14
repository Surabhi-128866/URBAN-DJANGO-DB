
import os
import django
import sys

# Setup Django environment
sys.path.append('c:\\Users\\SURABHI\\OneDrive\\Desktop\\urban-django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urban_habitat.settings')
django.setup()

from analyzer.models import Habitat

def fix_images():
    print("Fixing habitat images...")
    habitats = Habitat.objects.all()
    count = 0
    
    # Reliable City Image URL (Unsplash)
    new_image_url = "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&q=80"
    
    for habitat in habitats:
        print(f"Updating image for: {habitat.name}")
        # Force update the image URL
        habitat.image_url = new_image_url
        habitat.save()
        count += 1
        
    print(f"Successfully updated {count} habitats with reliable images.")

if __name__ == "__main__":
    fix_images()
