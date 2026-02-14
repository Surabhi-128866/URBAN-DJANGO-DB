import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "urban_habitat.settings")
django.setup()

from django.contrib.auth.models import User
from analyzer.models import Habitat

def test_constraints():
    # Setup users
    u1, _ = User.objects.get_or_create(username='user1')
    u2, _ = User.objects.get_or_create(username='user2')

    # Clean up previous runs
    Habitat.objects.filter(name='TestCity').delete()

    print("Creating 'TestCity' for user1...")
    h1 = Habitat.objects.create(name='TestCity', user=u1, population_density=100, crime_rate=1, green_space=50)
    print("Success.")

    print("Creating 'TestCity' for user2 (Should Succeed)...")
    try:
        h2 = Habitat.objects.create(name='TestCity', user=u2, population_density=200, crime_rate=2, green_space=40)
        print("Success: Different users can have same city name.")
    except Exception as e:
        print(f"FAILED: {e}")

    print("Creating 'TestCity' for user1 AGAIN (Should Fail)...")
    try:
        h3 = Habitat.objects.create(name='TestCity', user=u1, population_density=300, crime_rate=3, green_space=30)
        print("FAILED: Duplicate created for same user!")
    except Exception as e:
        print(f"Success: Correctly blocked duplicate for same user. Error: {e}")

if __name__ == "__main__":
    test_constraints()
