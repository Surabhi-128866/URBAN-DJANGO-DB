import requests

def test_wiki_search(query):
    print(f"--- Testing Query: '{query}' ---")
    
    # 1. Current Method: list=search
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": 5,
        "origin": "*"
    }
    try:
        data = requests.get(url, params=params).json()
        results = [r['title'] for r in data.get('query', {}).get('search', [])]
        print(f"Current (list=search): {results}")
    except Exception as e:
        print(f"Current Error: {e}")

    # 2. OpenSearch (Suggestion/Autocomplete)
    # Action=opensearch is designed for this.
    params_open = {
        "action": "opensearch",
        "format": "json",
        "search": query,
        "limit": 5,
        "origin": "*"
    }
    try:
        data = requests.get(url, params=params_open).json()
        # [search_term, [titles], [descriptions], [links]]
        results = data[1] if len(data) > 1 else []
        print(f"OpenSearch: {results}")
    except Exception as e:
        print(f"OpenSearch Error: {e}")
        
    # 3. PrefixSearch
    params_prefix = {
        "action": "query",
        "format": "json",
        "list": "prefixsearch",
        "pssearch": query,
        "pslimit": 5,
        "origin": "*"
    }
    try:
        data = requests.get(url, params=params_prefix).json()
        results = [r['title'] for r in data.get('query', {}).get('prefixsearch', [])]
        print(f"PrefixSearch: {results}")
    except Exception as e:
        print(f"PrefixSearch Error: {e}")

if __name__ == "__main__":
    test_wiki_search("Hyderabd,India")
    test_wiki_search("Hyderabd") # Typo without comma
