import requests

def test_overpass(query):
    print(f"Testing Overpass for: '{query}'")
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json][timeout:25];
    nwr["name"~"{query}", i];
    out center 1;
    """
    try:
        response = requests.get(overpass_url, params={'data': overpass_query}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            elements = data.get('elements', [])
            if elements:
                print(f"SUCCESS: Found {len(elements)} elements.")
                el = elements[0]
                lat = el.get('lat') or el.get('center', {}).get('lat')
                lon = el.get('lon') or el.get('center', {}).get('lon')
                print(f"Coords: {lat}, {lon}")
                print(f"Name: {el.get('tags', {}).get('name')}")
            else:
                print("FAILURE: No elements found.")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_overpass("TKR College")
