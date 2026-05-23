import json
from signals import search_jewelry, search_trends, search_macro
from store import create_table, store_results, show_listings
from brain import analyze_market
from publisher import publish_report

def run():
    print("=== RAVEN MARKET AGENT ===\n")
    
    # 1. Create table if needed
    create_table()
    
    # 2. Gather signals
    print("Scanning macro signals...")
    macro = search_macro()
    macro_text = "\n".join([f"{r['title']}: {r['description']}" for r in macro.get("results", [])[:3]])
    
    print("Scanning jewelry market...")
    queries = [
        "antique Victorian mourning ring for sale",
        "Georgian gold ring antique dealer",
        "Art Deco jewelry estate sale"
    ]
    
    all_results = []
    for q in queries:
        print(f"  Searching: {q}")
        results = search_jewelry(q, num_results=5)
        store_results(results, q)
        for r in results.get("results", []):
            all_results.append(f"{r['title']}: {r['description']}")
    
    listings_text = "\n".join(all_results)
    
    # 3. Brain analyzes
    print("\nAnalyzing market...")
    report = analyze_market(listings_text, macro_text)
    print("\n" + report)
    
    # 4. Publish to Senso
    print("\nPublishing report...")
    publish_report("RAVEN Market Intelligence Brief", report)
    
    # 5. Show stored listings
    print("\nStored listings:")
    show_listings()
    
    print("\n=== AGENT RUN COMPLETE ===")

if __name__ == "__main__":
    run()
