import anthropic
from config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def analyze_market(listings, macro_data=None):
    prompt = f"""You are RAVEN Market, an autonomous antique jewelry market intelligence agent.

Analyze these search results and generate a market brief. Consider:
- Which pieces are potentially underpriced
- Which dealers have multiple listings (bulk deal opportunity)  
- Small eBay sellers who may not have repriced with gold fluctuations
- Current macro conditions if provided

Search results:
{listings}

Macro signals:
{macro_data or 'Not available'}

Generate a concise market report with:
1. Market conditions summary
2. Top 3 buy opportunities with reasoning
3. Recommended search queries for next scan
"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

if __name__ == "__main__":
    test_listings = "Fetheray: Georgian mourning ring, 1200 GBP. 1stDibs: 12 mourning rings, 793-2709 USD. Etsy: high volume, mixed quality. AJC: large selection, free shipping."
    report = analyze_market(test_listings, "S&P up 0.17%, gold stable")
    print(report)
