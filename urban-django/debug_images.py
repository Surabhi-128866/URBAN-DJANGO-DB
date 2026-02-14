
import requests
import json

def get_wiki_image_debug(query):
    print(f"\n--- Testing Query: '{query}' ---")
    url = "https://en.wikipedia.org/w/api.php"
    
    # 1. Try SEARCH query
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": query,
        "gsrlimit": 1,
        "prop": "pageimages",
        "pithumbsize": 1000,
        "origin": "*"
    }
    
    headers = {
        "User-Agent": "UrbanHabitatAnalyzer/1.0 (contact@example.com)"
    }
    
    try:
        print(f"Requesting Wiki for: {query}")
        response = requests.get(url, params=params, headers=headers, timeout=5)
        data = response.json()
        print("Response Keys:", data.keys())
        
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            print(f"Page ID: {page_id}, Title: {page_data.get('title', 'Unknown')}")
            if page_id == "-1":
                print(" -> No page found.")
                return None
            
            if "thumbnail" in page_data:
                img_url = page_data["thumbnail"]["source"]
                print(f" -> FOUND IMAGE: {img_url}")
                return img_url
            else:
                print(" -> Page found, but NO thumbnail image.")
                
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Test the problematic locations
    get_wiki_image_debug("Tkr Engineering College")
    get_wiki_image_debug("Hyderabad")
    get_wiki_image_debug("China")
    get_wiki_image_debug("Meerpet")
