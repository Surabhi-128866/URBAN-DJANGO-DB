
import requests
import time

def test_url(name, url, params=None):
    print(f"Testing {name}...")
    start = time.time()
    try:
        response = requests.get(url, params=params, timeout=10, headers={'User-Agent': 'TestScript/1.0'})
        elapsed = time.time() - start
        print(f"  Status: {response.status_code}")
        print(f"  Time: {elapsed:.2f}s")
        if response.status_code == 200:
            print("  SUCCESS")
            return True
        else:
            print("  FAILED (Status Code)")
            return False
    except Exception as e:
        print(f"  FAILED (Exception): {e}")
        return False

def run_tests():
    print("--- STARTING API TESTS ---")
    
    # 1. Wikipedia Search
    test_url("Wikipedia Search", "https://en.wikipedia.org/w/api.php", 
             params={"action": "query", "list": "search", "srsearch": "Hyderabad", "format": "json"})

    # 2. Nominatim (Coordinates)
    test_url("Nominatim", "https://nominatim.openstreetmap.org/search", 
             params={"q": "Hyderabad", "format": "json", "limit": 1})

    # 3. Overpass API
    test_url("Overpass API", "https://overpass-api.de/api/interpreter",
             params={"data": "[out:json];node(around:100,17.3850,78.4867)[amenity=restaurant];out;"})

if __name__ == "__main__":
    run_tests()
