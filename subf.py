import requests
import sys
import re

def main():
    domain = input("Domain: ").strip().lower()
    output = input("Output file [results.txt]: ").strip()

    if not domain:
        return

    if not output:
        output = "results.txt"

    domain = domain.removeprefix("https://").removeprefix("http://").rstrip("/")
    url = f"https://crt.name/v1/search?apex={domain}"

    try:
        res = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20
        )
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"\nRequest failed: {e}")
        return

    try:
        data = res.json()
        text = "\n".join(item.get("name", "") for item in data)
    except ValueError:
        text = res.text

    subs = set()

    for sub in re.findall(
        rf"(?:\*\.)?(?:[a-zA-Z0-9_-]+\.)+{re.escape(domain)}",
        text
    ):
        sub = sub.lower().rstrip(".")
        sub = sub.removeprefix("*.")

        while sub.startswith("www."):
            sub = sub[4:]

        if sub != domain:
            subs.add(sub)

    subs = sorted(subs)

    with open(output, "w", encoding="utf-8") as f:
        f.write("\n".join(subs))

    print(f"\nDone. Found {len(subs)} unique subdomains.")
    print(f"Saved to: {output}")


if __name__ == "__main__":
    main()
