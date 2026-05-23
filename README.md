# RAVEN Market

**Autonomous antique jewelry market intelligence agent**

Built at Agentic Engineering Hack, Datadog NYC, May 2026

## What it does

RAVEN Market reads the economy, reads the culture, and tells antique jewelry dealers what to buy this week and who's going to buy it from them.

## How it works

1. **Nimble** scrapes macro signals (S&P, gold, VIX) and dealer listings across the open web
2. **Claude** reads the signals and generates a buy strategy based on economy logic:
   - Stocks up → buy heavy gold (buyers feel flush, gold may be dipping)
   - Stocks down → buy cameos and silver (only appetite in a scared market)
   - Bad news dominating → BUY (retail freezes, dealers get desperate, prices drop)
3. **ClickHouse** stores every listing with price, dealer, era, and timestamps for trend analysis
4. **Senso** publishes grounded, citeable market reports to the agentic web

## Scoring intelligence

- Dealers with multiple listings flagged for bulk negotiation
- Small eBay sellers who haven't repriced with gold fluctuations (arbitrage)
- Listings older than 30 days (motivated sellers)

## Who is this for

Antique dealers, flippers, booth operators, Instagram retailers. The person driving home from Brimfield at 11 PM wondering what she missed — this agent already found it.

## Tech stack

- Nimble API (web search + scraping)
- ClickHouse Cloud (analytical database)
- Senso AI (knowledge base + publishing)
- Claude API (market analysis brain)
- Python

## Run it

```
python3 agent.py
python3 dashboard.py
open dashboard.html
```
