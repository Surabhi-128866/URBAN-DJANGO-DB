
import os
import django
import sys

# Setup Django environment
sys.path.append('c:\\Users\\SURABHI\\OneDrive\\Desktop\\urban-django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urban_habitat.settings')
django.setup()

from analyzer.utils import get_habitat_data

def test_search():
    # Test a definitely wrong location
    query = "Hydrabaddfdfef" 
    print(f"Testing search for: {query}")
    data = get_habitat_data(query)
    print("Result:", data)
    
    # Test a typo location that should have suggestions
    query2 = "Hydrabad"
    print(f"\nTesting search for: {query2}")
    data2 = get_habitat_data(query2)
    print("Result:", data2)

if __name__ == "__main__":
    test_search()
