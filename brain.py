import anthropic
from config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def analyze_market(listings, macro_data=None):
    prompt = f"""You are RAVEN Market, an autonomous antique jewelry market intelligence agent built for dealers, flippers, and booth operators.

ECONOMY LOGIC:
- If stocks are up/trending up: buyers feel flush. Look for HEAVY gold pieces, statement jewelry, high-ticket items. Gold spot may be dipping (inverse correlation) so acquisition cost is lower.
- If stocks are down/economy is garbage: look for CAMEOS, SILVER, affordable pieces. That is the only appetite. Skip the $15K rings.
- If gold is dipping while stocks are stable: BUY gold pieces to hold. The spread between purchase and melt is favorable.
- If negative news dominates (oil spikes, political chaos): BUY BUY BUY. Retail buyers freeze, dealers get desperate, prices drop. Contrarian signal.

SCORING BOOSTS:
- Dealers with MULTIPLE listings: flag for bulk deal negotiation
- Small eBay sellers: likely have NOT repriced with gold fluctuations. Arbitrage opportunity.
- Listings older than 30 days: seller may be motivated

Analyze these search results and macro signals. Generate a market brief.

Search results:
{listings}

Macro signals:
{macro_data or 'Not available'}

Generate:
1. Economy read (bull/bear/neutral) and what that means for buying strategy
2. Top 3 buy opportunities with reasoning
3. Bulk deal opportunities (dealers with multiple listings)
4. Lazy repricer alerts (small sellers who havent adjusted)
5. Recommended search queries for next scan
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
