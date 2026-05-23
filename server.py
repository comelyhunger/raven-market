from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import markdown
from signals import search_jewelry, search_macro
from brain import analyze_market
from store import create_table, store_results, get_client

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            query = params.get("q", [None])[0]
            html = build_dashboard(query)
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()
    def log_message(self, format, *args):
        pass

def build_dashboard(user_query=None):
    create_table()
    macro = search_macro()
    macro_text = "\n".join([f"{r['title']}: {r['description']}" for r in macro.get("results", [])[:3]])
    if user_query:
        queries = [user_query]
    else:
        queries = ["antique Victorian mourning ring for sale", "Georgian gold ring antique dealer", "Art Deco jewelry estate sale"]
    all_results = []
    for q in queries:
        results = search_jewelry(q, num_results=10)
        store_results(results, q)
        for r in results.get("results", []):
            all_results.append(r)
    listings_text = "\n".join([f"{r['title']}: {r['description']}" for r in all_results])
    report = analyze_market(listings_text, macro_text)
    report_html = markdown.markdown(report)
    by_source = {}
    for r in all_results:
        source = r.get("url", "").split("/")[2] if "/" in r.get("url", "") else "Unknown"
        source = source.replace("www.", "")
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(r)
    listings_html = ""
    for item in all_results:
        title = item.get("title", "No title")[:50]
        desc = item.get("description", "")[:80]
        url = item.get("url", "#")
        source = item.get("url", "").split("/")[2].replace("www.", "") if "/" in item.get("url", "") else ""
        listings_html += f'''<a href="{url}" target="_blank" class="item-card">
            <div class="item-title">{title}</div>
            <div class="item-source">{source}</div>
            <div class="item-desc">{desc}</div>
        </a>'''
    query_display = user_query if user_query else "Victorian mourning, Georgian gold, Art Deco"
    safe_query = user_query or ""
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>RAVEN Market</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:#f4f1eb;color:#2a2520}}
.header{{background:#2a1f14;padding:14px 30px;display:flex;align-items:center;justify-content:space-between}}
.header h1{{font-family:Georgia,serif;font-size:20px;color:#c9a84c;letter-spacing:2px}}
.header .right{{display:flex;align-items:center;gap:16px}}
.header span{{color:#8a7d6b;font-size:11px;letter-spacing:1px}}
.badge{{display:inline-block;background:#3d3428;color:#c9a84c;padding:2px 8px;border-radius:10px;font-size:10px;margin:0 2px}}
.toolbar{{background:#fff;border-bottom:1px solid #e0dcd4;padding:12px 30px;display:flex;align-items:center;gap:16px}}
.search-form{{display:flex;gap:6px;flex:1;max-width:500px}}
.search-form input{{flex:1;padding:8px 12px;border:1px solid #d4cfc4;border-radius:4px;font-size:13px;background:#faf8f4}}
.search-form button{{padding:8px 16px;background:#2a1f14;color:#c9a84c;border:none;border-radius:4px;font-size:12px;font-weight:bold;cursor:pointer}}
.search-form button:hover{{background:#3d3428}}
.toolbar .stats{{display:flex;gap:16px;font-size:12px;color:#8a7d6b}}
.toolbar .stats b{{color:#2a1f14;font-size:14px}}
.container{{max-width:1400px;margin:0 auto;padding:20px 30px}}
.section-title{{font-family:Georgia,serif;font-size:15px;color:#6b5d3e;margin:16px 0 10px;text-transform:uppercase;letter-spacing:1px}}
.listings-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}}
.item-card{{background:#fff;border:1px solid #e0dcd4;border-radius:6px;padding:14px;text-decoration:none;display:block;transition:all 0.2s}}
.item-card:hover{{border-color:#c9a84c;box-shadow:0 2px 8px rgba(0,0,0,0.06)}}
.item-title{{font-size:13px;font-weight:700;color:#2a1f14;margin-bottom:4px;line-height:1.3}}
.item-source{{font-size:11px;color:#c9a84c;margin-bottom:6px;font-weight:600}}
.item-desc{{font-size:11px;color:#888;line-height:1.4}}
.two-col{{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-top:16px}}
.report{{background:#fff;border:1px solid #e0dcd4;border-radius:6px;padding:20px}}
.report h1{{font-size:16px;color:#2a1f14;margin:10px 0 6px}}
.report h2{{font-size:14px;color:#6b5d3e;margin:8px 0 4px}}
.report h3{{font-size:12px;color:#8a7d6b;margin:6px 0 4px}}
.report p{{font-size:12px;line-height:1.7;margin:4px 0}}
.report ul,.report ol{{padding-left:16px;margin:4px 0}}
.report li{{font-size:12px;line-height:1.5}}
.report strong{{color:#2a1f14}}
.report code{{background:#f4f1eb;padding:1px 4px;border-radius:2px;font-size:11px}}
.how-box{{background:#fff;border:1px solid #e0dcd4;border-radius:6px;padding:16px}}
.how-box h3{{font-family:Georgia,serif;font-size:13px;color:#6b5d3e;margin-bottom:10px}}
.step{{display:flex;gap:8px;margin-bottom:8px;font-size:12px;line-height:1.5}}
.step-n{{background:#2a1f14;color:#c9a84c;width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:bold;flex-shrink:0}}
.step-t{{color:#555}}
.step-t b{{color:#2a1f14}}
.footer{{text-align:center;padding:16px;color:#bbb;font-size:11px}}
</style>
</head>
<body>
<div class="header">
<h1>RAVEN MARKET</h1>
<div class="right">
<span>ANTIQUE JEWELRY INTELLIGENCE</span>
<span class="badge">Nimble</span>
<span class="badge">ClickHouse</span>
<span class="badge">Senso</span>
<span class="badge">Claude</span>
</div>
</div>
<div class="toolbar">
<form class="search-form" action="/" method="get">
<input type="text" name="q" placeholder="Search: e.g. Georgian mourning ring, Art Deco bracelet, Victorian cameo..." value="{safe_query}">
<button type="submit">Search</button>
</form>
<div class="stats">
<span><b>{len(all_results)}</b> listings</span>
<span><b>{len(by_source)}</b> dealers</span>
<span><b>6</b> signals</span>
</div>
</div>
<div class="container">
<div class="section-title">Listings found</div>
<div class="listings-grid">
{listings_html}
</div>
<div class="two-col">
<div class="report">
<div class="section-title" style="margin-top:0">Market intelligence report</div>
{report_html}
</div>
<div class="how-box">
<h3>How RAVEN Market works</h3>
<div class="step"><div class="step-n">1</div><div class="step-t"><b>Read the economy</b> — S&amp;P, gold, VIX, news sentiment</div></div>
<div class="step"><div class="step-n">2</div><div class="step-t"><b>Scan the web</b> — Nimble searches dealers, auctions, eBay</div></div>
<div class="step"><div class="step-n">3</div><div class="step-t"><b>Analyze</b> — Claude reads signals, flags opportunities</div></div>
<div class="step"><div class="step-n">4</div><div class="step-t"><b>Store</b> — ClickHouse tracks prices over time</div></div>
<div class="step"><div class="step-n">5</div><div class="step-t"><b>Publish</b> — Senso publishes citeable reports</div></div>
<h3 style="margin-top:16px">Economy logic</h3>
<div class="step"><div class="step-t">Stocks up = buy heavy gold<br>Stocks down = buy cameos, silver<br>Bad news = BUY (dealers panic)<br>Gold dip = hold inventory</div></div>
<h3 style="margin-top:16px">Smart scoring</h3>
<div class="step"><div class="step-t">Multiple listings = bulk deal<br>Small eBay sellers = lazy repricers<br>30+ day listings = motivated sellers</div></div>
</div>
</div>
</div>
<div class="footer">RAVEN MARKET — Built at Agentic Engineering Hack, Datadog NYC, May 2026</div>
</body>
</html>"""

print("RAVEN Market running at http://localhost:8000")
HTTPServer(("", 8000), Handler).serve_forever()
