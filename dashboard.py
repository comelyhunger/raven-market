import json
import markdown
from signals import search_jewelry, search_macro
from brain import analyze_market
from store import create_table, store_results, get_client

def generate_dashboard(user_query=None):
    create_table()
    
    print("Gathering signals...")
    macro = search_macro()
    macro_text = "\n".join([f"{r['title']}: {r['description']}" for r in macro.get("results", [])[:3]])
    
    if user_query:
        queries = [user_query]
    else:
        queries = [
            "antique Victorian mourning ring for sale",
            "Georgian gold ring antique dealer",
            "Art Deco jewelry estate sale"
        ]
    
    all_results = []
    for q in queries:
        print(f"  Searching: {q}")
        results = search_jewelry(q, num_results=10)
        store_results(results, q)
        for r in results.get("results", []):
            all_results.append(r)
    
    listings_text = "\n".join([f"{r['title']}: {r['description']}" for r in all_results])
    
    print("Analyzing market...")
    report = analyze_market(listings_text, macro_text)
    report_html = markdown.markdown(report)
    
    # Group listings by source
    by_source = {}
    for r in all_results:
        source = r.get("url", "").split("/")[2] if "/" in r.get("url", "") else "Unknown"
        source = source.replace("www.", "")
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(r)
    
    # Build listing cards HTML
    listings_html = ""
    for source, items in sorted(by_source.items()):
        listings_html += f'<div class="source-group"><h3>{source} ({len(items)} listings)</h3>'
        for item in items:
            title = item.get("title", "No title")[:80]
            desc = item.get("description", "")[:150]
            url = item.get("url", "#")
            listings_html += f"""
            <div class="listing-card">
                <a href="{url}" target="_blank" class="listing-title">{title}</a>
                <p class="listing-desc">{desc}</p>
                <a href="{url}" target="_blank" class="shop-btn">View Listing</a>
            </div>"""
        listings_html += "</div>"
    
    query_display = user_query if user_query else "Victorian mourning, Georgian gold, Art Deco"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>RAVEN Market Intelligence</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Georgia', serif; background: #0a0a0a; color: #e8e0d4; }}
.header {{ background: linear-gradient(135deg, #1a1510, #2a1f14); padding: 40px; border-bottom: 2px solid #c9a84c; }}
.header h1 {{ font-size: 36px; color: #c9a84c; letter-spacing: 3px; }}
.header p {{ color: #8a7d6b; margin-top: 8px; font-size: 14px; letter-spacing: 1px; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 30px; }}

.search-box {{ background: #141210; border: 1px solid #2a2520; border-radius: 8px; padding: 24px; margin-top: 24px; }}
.search-box h2 {{ color: #c9a84c; font-size: 16px; margin-bottom: 12px; }}
.search-box input {{ width: 70%; padding: 12px 16px; background: #1a1815; border: 1px solid #3d3428; border-radius: 6px; color: #e8e0d4; font-size: 14px; font-family: Georgia, serif; }}
.search-box button {{ padding: 12px 24px; background: #c9a84c; color: #0a0a0a; border: none; border-radius: 6px; font-size: 14px; font-weight: bold; cursor: pointer; margin-left: 8px; font-family: Georgia, serif; }}
.search-box button:hover {{ background: #d4b65c; }}
.search-box .current {{ color: #8a7d6b; font-size: 12px; margin-top: 8px; }}

.stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 24px; }}
.stat {{ background: #141210; border: 1px solid #2a2520; border-radius: 8px; text-align: center; padding: 20px; }}
.stat .number {{ font-size: 36px; color: #c9a84c; font-weight: bold; }}
.stat .label {{ color: #8a7d6b; font-size: 11px; margin-top: 4px; letter-spacing: 1px; }}

.section {{ background: #141210; border: 1px solid #2a2520; border-radius: 8px; padding: 24px; margin-top: 24px; }}
.section h2 {{ color: #c9a84c; font-size: 18px; margin-bottom: 16px; border-bottom: 1px solid #2a2520; padding-bottom: 8px; }}
.section h1 {{ color: #e8e0d4; font-size: 22px; margin: 16px 0 8px; }}
.section h2 {{ color: #c9a84c; }}
.section h3 {{ color: #d4b65c; margin: 12px 0 6px; }}
.section strong {{ color: #e8e0d4; }}
.section ul, .section ol {{ padding-left: 20px; margin: 8px 0; }}
.section li {{ margin: 4px 0; line-height: 1.6; }}
.section p {{ line-height: 1.8; margin: 8px 0; }}
.section code {{ background: #1a1815; padding: 2px 6px; border-radius: 3px; font-size: 13px; }}

.source-group {{ margin-top: 20px; }}
.source-group h3 {{ color: #c9a84c; font-size: 14px; margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1px solid #2a2520; }}
.listing-card {{ background: #1a1815; border: 1px solid #2a2520; border-radius: 6px; padding: 16px; margin-bottom: 10px; display: flex; flex-direction: column; gap: 6px; }}
.listing-title {{ color: #e8e0d4; font-size: 14px; text-decoration: none; font-weight: bold; }}
.listing-title:hover {{ color: #c9a84c; }}
.listing-desc {{ color: #8a7d6b; font-size: 12px; line-height: 1.5; }}
.shop-btn {{ display: inline-block; background: #2a1f14; color: #c9a84c; padding: 6px 16px; border-radius: 4px; font-size: 12px; text-decoration: none; align-self: flex-start; margin-top: 4px; }}
.shop-btn:hover {{ background: #3d3428; }}

.badge {{ display: inline-block; background: #2a1f14; color: #c9a84c; padding: 4px 12px; border-radius: 12px; font-size: 11px; margin: 2px; }}
.tools {{ text-align: center; margin-top: 24px; padding: 16px; }}
.tools span {{ margin: 0 4px; }}
.footer {{ text-align: center; padding: 30px; color: #3d3428; font-size: 12px; }}

.how-it-works {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 24px; }}
.step {{ background: #141210; border: 1px solid #2a2520; border-radius: 8px; padding: 20px; }}
.step .step-num {{ font-size: 28px; color: #c9a84c; font-weight: bold; }}
.step .step-title {{ color: #e8e0d4; font-size: 14px; font-weight: bold; margin: 8px 0 4px; }}
.step .step-desc {{ color: #8a7d6b; font-size: 12px; line-height: 1.5; }}
</style>
</head>
<body>
<div class="header">
<h1>RAVEN MARKET</h1>
<p>AUTONOMOUS ANTIQUE JEWELRY MARKET INTELLIGENCE</p>
</div>
<div class="container">

<div class="search-box">
<h2>What are you looking for?</h2>
<input type="text" placeholder="e.g. Georgian mourning ring, Art Deco platinum bracelet, Victorian cameo..." id="query">
<button onclick="alert('Run: python3 dashboard.py --query your-search')">Search</button>
<div class="current">Current scan: {query_display}</div>
</div>

<div class="stats">
<div class="stat"><div class="number">{len(all_results)}</div><div class="label">LISTINGS FOUND</div></div>
<div class="stat"><div class="number">{len(by_source)}</div><div class="label">DEALERS SCANNED</div></div>
<div class="stat"><div class="number">3</div><div class="label">SPONSOR TOOLS</div></div>
<div class="stat"><div class="number">6</div><div class="label">SIGNAL LAYERS</div></div>
</div>

<div class="how-it-works">
<div class="step">
<div class="step-num">1</div>
<div class="step-title">Read the economy</div>
<div class="step-desc">S&P, gold spot, VIX, news sentiment. Determines buy posture: heavy gold vs. silver and cameos.</div>
</div>
<div class="step">
<div class="step-num">2</div>
<div class="step-title">Scan the market</div>
<div class="step-desc">Nimble searches dealer sites, auctions, eBay. Finds listings, prices, availability across the open web.</div>
</div>
<div class="step">
<div class="step-num">3</div>
<div class="step-title">Generate intelligence</div>
<div class="step-desc">Claude analyzes signals, flags underpriced pieces, bulk deals, lazy repricers. Publishes via Senso.</div>
</div>
</div>

<div class="section">
<h2>Market Intelligence Report</h2>
{report_html}
</div>

<div class="section">
<h2>Browse Listings by Dealer</h2>
{listings_html}
</div>

<div class="tools">
<span class="badge">Nimble API</span>
<span class="badge">ClickHouse Cloud</span>
<span class="badge">Senso AI</span>
<span class="badge">Claude API</span>
</div>
</div>
<div class="footer">
RAVEN MARKET — Built at Agentic Engineering Hack, Datadog NYC, May 2026<br>
Predictive market intelligence for antique jewelry dealers, flippers, and booth operators
</div>
</body>
</html>"""
    
    with open("dashboard.html", "w") as f:
        f.write(html)
    print("Dashboard saved to dashboard.html")

if __name__ == "__main__":
    import sys
    query = None
    if "--query" in sys.argv:
        idx = sys.argv.index("--query")
        if idx + 1 < len(sys.argv):
            query = " ".join(sys.argv[idx+1:])
    generate_dashboard(query)