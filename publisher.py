import subprocess
import json

def publish_report(title, text):
    data = json.dumps({"title": title, "text": text})
    result = subprocess.run(
        ["senso", "kb", "create-raw", "--data", data, "--output", "json"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("Published to Senso KB")
        return result.stdout
    else:
        print("Senso error:", result.stderr)
        return None

if __name__ == "__main__":
    print("Testing Senso publish via CLI...")
    result = publish_report("RAVEN Market Report", "Victorian mourning rings showing increased availability across major dealers. Price range 793 to 2709 USD.")
    print(result)
