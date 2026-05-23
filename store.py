import clickhouse_connect
from config import CLICKHOUSE_HOST, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD

def get_client():
    return clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=8443,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        secure=True
    )

def create_table():
    client = get_client()
    client.command("""
        CREATE TABLE IF NOT EXISTS listings (
            id UUID DEFAULT generateUUIDv4(),
            title String,
            description String,
            url String,
            source String,
            price Float64 DEFAULT 0,
            currency String DEFAULT 'USD',
            era String DEFAULT '',
            category String DEFAULT '',
            materials String DEFAULT '',
            search_query String,
            found_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY found_at
    """)
    print("Table 'listings' ready.")

def store_results(results, query):
    client = get_client()
    rows = []
    for item in results.get("results", []):
        rows.append([
            item.get("title", ""),
            item.get("description", ""),
            item.get("url", ""),
            item.get("url", "").split("/")[2] if "/" in item.get("url", "") else "",
            query
        ])
    if rows:
        client.insert("listings",
            rows,
            column_names=["title", "description", "url", "source", "search_query"]
        )
        print(f"Stored {len(rows)} listings.")

def show_listings():
    client = get_client()
    result = client.query("SELECT title, source, search_query, found_at FROM listings ORDER BY found_at DESC LIMIT 10")
    for row in result.result_rows:
        print(f"  {row[0][:60]} | {row[1]} | {row[3]}")

if __name__ == "__main__":
    create_table()
    from signals import search_jewelry
    results = search_jewelry("antique Victorian gold mourning ring")
    store_results(results, "antique Victorian gold mourning ring")
    print("\nStored listings:")
    show_listings()
