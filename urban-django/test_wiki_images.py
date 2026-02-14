
import requests

def get_wiki_image(query):
    print(f"Searching for image for: {query}")
    # clean query
    query = query.split(',')[0].strip() # Take "Hyderabad" from "Hyderabad, India"
    
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "titles": query,
        "pithumbsize": 800,
        "redirects": 1  # Follow redirects (e.g. "NYC" -> "New York City")
    }
    
    headers = {
        "User-Agent": "UrbanHabitatAnalyzer/1.0 (contact@example.com)"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        # print(f"Status: {response.status_code}")
        # print(f"Response: {response.text[:200]}...") # Debug preview
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if page_id == "-1":
                print(f"No wikipedia page found for {query}")
                return None
            
            if "thumbnail" in page_data:
                image_url = page_data["thumbnail"]["source"]
                print(f"Found image: {image_url}")
                return image_url
            else:
                print(f"Page found but no main image for {query}")
                
    except Exception as e:
        print(f"Error: {e}")
        
    return None

if __name__ == "__main__":
    print(get_wiki_image("Hyderabad"))
    print(get_wiki_image("Paris"))
    print(get_wiki_image("TKR College of Engineering and Technology")) # Likely won't exist or will be obscure
    print(get_wiki_image("NonExistentPlace123"))
