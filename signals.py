import requests
from config import NIMBLE_API_KEY

def search_jewelry(query, num_results=10):
    """Search for antique jewelry listings via Nimble"""
    url = "https://nimble-retriever.webit.live/search"
    headers = {
        "Authorization": f"Bearer {NIMBLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "query": query,
        "num_results": num_results,
        "deep_search": False,
        "country": "US",
        "locale": "en"
    }
    resp = requests.post(url, headers=headers, json=data)
    resp.raise_for_status()
    return resp.json()

def search_trends(query="antique jewelry trends 2026"):
    """Search for trend signals via Nimble"""
    return search_jewelry(query, num_results=5)

def search_macro(query="S&P 500 gold price today"):
    """Search for macro economic signals via Nimble"""
    return search_jewelry(query, num_results=5)

if __name__ == "__main__":
    print("Testing jewelry search...")
    results = search_jewelry("antique Victorian gold mourning ring for sale")
    for item in results.get("results", []):
        print(f"  {item.get('title', 'No title')}")
        print(f"  {item.get('url', '')}")
        print(f"  {item.get('description', '')}")
        print()
