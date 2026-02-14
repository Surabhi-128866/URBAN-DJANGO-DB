import requests

def test_bing_image(query):
    url = f"https://tse2.mm.bing.net/th?q={query}&w=800&h=600&c=7&rs=1&p=0"
    try:
        response = requests.get(url, timeout=5)
        print(f"Status for '{query}': {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
            print("SUCCESS: Image found.")
        else:
            print("FAILURE: No image or error.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_bing_image("TKR Engineering College")
    test_bing_image("Mumbai")
