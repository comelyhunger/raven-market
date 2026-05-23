import json
import markdown
from signals import search_jewelry, search_macro
from brain import analyze_market
from store import create_table, store_results, get_client

def generate_dashboard():
    create_table()
    
    print("Gathering signals...")
    macro = search_macro()
    macro_text = "\n".join([f"{r['title']}: {r['description']}" for r in macro.get("results", [])[:3]])
    
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
            all_results.append(r)
    
    listings_text = "\n".join([f"{r['title']}: {r['description']}" for r in all_results])
    
    print("Analyzing market...")
    report = analyze_market(listings_text, macro_text)
    
    # Get stored listings from ClickHouse
    client = get_client()
    db_results = client.query("SELECT title, source, url, search_query, found_at FROM listings ORDER BY found_at DESC LIMIT 30")
    
    listings_html = ""
    for row in db_results.result_rows:
        listings_html += f'<tr><td>{row[0][:60]}</td><td>{row[1]}</td><td><a href="{row[2]}" target="_blank">View</a></td><td>{row[3][:30]}</td></tr>\n'
    
    report_html = markdown.markdown(report)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>RAVEN Market Intelligence</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Georgia', serif; background: #0a0a0a; color: #e8e0d4; }}
.header {{ background: linear-gradient(135deg, #1a1510, #2a1f14); padding: 40px; border-bottom: 1px solid #3d3428; }}
.header h1 {{ font-size: 36px; color: #c9a84c; letter-spacing: 3px; }}
.header p {{ color: #8a7d6b; margin-top: 8px; font-size: 14px; letter-spacing: 1px; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 30px; }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 24px; }}
.card {{ background: #141210; border: 1px solid #2a2520; border-radius: 8px; padding: 24px; }}
.card h2 {{ color: #c9a84c; font-size: 18px; margin-bottom: 16px; border-bottom: 1px solid #2a2520; padding-bottom: 8px; }}
.report {{ grid-column: 1 / -1; font-size: 14px; line-height: 1.8; }}
.report br {{ margin-bottom: 4px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
th {{ text-align: left; color: #c9a84c; padding: 8px; border-bottom: 1px solid #2a2520; }}
td {{ padding: 8px; border-bottom: 1px solid #1a1815; color: #b8a88a; }}
a {{ color: #c9a84c; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.stat {{ text-align: center; padding: 20px; }}
.stat .number {{ font-size: 42px; color: #c9a84c; font-weight: bold; }}
.stat .label {{ color: #8a7d6b; font-size: 12px; margin-top: 4px; letter-spacing: 1px; }}
.badge {{ display: inline-block; background: #2a1f14; color: #c9a84c; padding: 4px 12px; border-radius: 12px; font-size: 11px; margin: 2px; }}
.footer {{ text-align: center; padding: 30px; color: #3d3428; font-size: 12px; }}
</style>
</head>
<body>
<div class="header">
<h1>RAVEN MARKET</h1>
<p>AUTONOMOUS ANTIQUE JEWELRY MARKET INTELLIGENCE</p>
</div>
<div class="container">
<div class="grid">
<div class="card stat">
<div class="number">{len(all_results)}</div>
<div class="label">LISTINGS SCANNED</div>
</div>
<div class="card stat">
<div class="number">{len(queries)}</div>
<div class="label">SEARCH QUERIES</div>
</div>
<div class="card stat">
<div class="number">3</div>
<div class="label">SPONSOR TOOLS</div>
</div>
<div class="card stat">
<div class="number">6</div>
<div class="label">SIGNAL LAYERS</div>
</div>
</div>
<div class="card report" style="margin-top:24px;">
<h2>Market Intelligence Report</h2>
{report_html}
</div>
<div class="card" style="margin-top:24px;">
<h2>Listings Database (ClickHouse)</h2>
<table>
<tr><th>Title</th><th>Source</th><th>Link</th><th>Query</th></tr>
{listings_html}
</table>
</div>
<div style="margin-top:24px; text-align:center;">
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
    generate_dashboard() 
