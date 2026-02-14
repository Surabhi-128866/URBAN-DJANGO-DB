import os
import django
from django.conf import settings

# Configure Django settings manually since we are running a standalone script
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=['analyzer'],
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db.sqlite3'}},
    )
    django.setup()

from analyzer.utils import get_habitat_data, get_wikipedia_image

locations = ["Hyderabad", "New York", "DoesNotExistCity123"]

print("--- Testing Image Fetching ---")
for loc in locations:
    print(f"\nTesting: {loc}")
    img = get_wikipedia_image(loc)
    print(f"Wikipedia Image: {img}")
    
    data = get_habitat_data(loc)
    print(f"Final Data Image URL: {data['image_url']}")
