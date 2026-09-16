import requests
import socket
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed


def pickFolder():
    name = input("Results folder [results]: ").strip() or "results"
    os.makedirs(name, exist_ok=True)
    return name


def findSubdomains(folder):
    domain = input("Domain: ").strip().lower()
    if not domain:
        return None

    domain = domain.removeprefix("https://").removeprefix("http://").rstrip("/")

    name = input("Save subdomains as [subdomains.txt]: ").strip() or "subdomains.txt"
    if not name.endswith(".txt"):
        name += ".txt"
    output = os.path.join(folder, name)

    url = f"https://crt.name/v1/search?apex={domain}"

    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"\nRequest failed: {e}")
        return None

    try:
        data = res.json()
        text = "\n".join(item.get("name", "") for item in data)
    except ValueError:
        text = res.text

    found = set()
    for sub in re.findall(rf"(?:\*\.)?(?:[a-zA-Z0-9_-]+\.)+{re.escape(domain)}", text):
        sub = sub.lower().rstrip(".")
        sub = sub.removeprefix("*.")
        while sub.startswith("www."):
            sub = sub[4:]
        if sub != domain:
            found.add(sub)

    if not found:
        print("\nNo subdomains found.")
        return None

    print(f"\nFound {len(found)} unique subdomains")
    print("[1] Sort A to Z")
    print("[2] Sort Z to A")

    while True:
        pick = input("Choice [1]: ").strip() or "1"
        if pick in ("1", "2"):
            break
        print("Enter 1 or 2.")

    subs = sorted(found, reverse=(pick == "2"))

    with open(output, "w", encoding="utf-8") as f:
        f.write("\n".join(subs))

    print(f"Saved to: {output}")
    return output


def resolveOne(domain):
    try:
        results = socket.getaddrinfo(domain, None, socket.AF_INET, socket.SOCK_STREAM)
        ips = {result[4][0] for result in results}
        if ips:
            return domain, ips, None
        return domain, set(), "no ip"
    except socket.gaierror as e:
        return domain, set(), str(e)


def resolveDomains(folder, path):
    print("\n[1] List only IP addresses")
    print("[2] List domains after each IP address")

    while True:
        choice = input("Choice: ").strip()
        if choice in ("1", "2"):
            break
        print("Enter 1 or 2.")

    name = input("Output file [ips.txt]: ").strip() or "ips.txt"
    if not name.endswith(".txt"):
        name += ".txt"
    output = os.path.join(folder, name)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        domains = list({
            line.strip().lower()
            for line in f
            if line.strip() and not line.startswith("#")
        })

    if not domains:
        print("No domains found.")
        return

    workers = min(1000, len(domains))
    print(f"\nResolving {len(domains)} domains with {workers} workers...\n")

    resolved = {}
    dead = []
    done = 0
    total = len(domains)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        jobs = [pool.submit(resolveOne, d) for d in domains]
        for job in as_completed(jobs):
            domain, ips, error = job.result()
            done += 1

            if error:
                dead.append(domain)
            else:
                for ip in ips:
                    resolved.setdefault(ip, []).append(domain)

            if done % 25 == 0 or done == total:
                print(f"\rProgress: {done}/{total}", end="", flush=True)

    with open(output, "w", encoding="utf-8") as f:
        if choice == "1":
            f.write("\n".join(sorted(resolved)))
        else:
            for ip in sorted(resolved):
                for domain in sorted(resolved[ip]):
                    f.write(f"{ip} {domain}\n")

    print("\n")
    print("=" * 45)
    print(f"Unique IPs   : {len(resolved)}")
    print(f"Live domains : {total - len(dead)}")
    print(f"Dead domains : {len(dead)}")
    print(f"Output       : {output}")
    print("=" * 45)


def main():
    print("[1] Find subdomains")
    print("[2] Resolve a list of domains")
    print("[3] Find subdomains, then resolve them")
    print("[0] Exit")

    while True:
        pick = input("\nChoice: ").strip()
        if pick in ("0", "1", "2", "3"):
            break
        print("Enter 0, 1, 2, or 3.")

    if pick == "0":
        return

    if pick == "1":
        folder = pickFolder()
        findSubdomains(folder)
        return

    if pick == "2":
        folder = pickFolder()
        while True:
            path = input("Path to domains file: ").strip().strip('"')
            if os.path.isfile(path):
                break
            print("File not found.")
        resolveDomains(folder, path)
        return

    folder = pickFolder()
    subs = findSubdomains(folder)
    if subs:
        print("\nNow resolving the subdomains...")
        resolveDomains(folder, subs)


if __name__ == "__main__":
    main()
