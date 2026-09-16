# Subf

Small tool i threw together to find subdomains and resolve them to IPs. Does the whole thing in one flow if u want, or just the piece u need.

## What it does

- pulls subdomains from crt.name for a domain
- strips `www` and dupes, drops the apex itself
- lets u sort a to z or z to a before saving
- resolves a list of domains to IPs with threads
- can do both in one go, subdomains then straight into the resolver
- everything lands in a folder, default is `results`, you can name it whatever

## Usage

Just run it

```
python subf.py
```

You get a menu

```
[1] Find subdomains
[2] Resolve a list of domains
[3] Find subdomains, then resolve them
[0] Exit
```

Pick a number, answer the questions, done.

## the options

**1. find subdomains**

Asks for a domain, hits crt.name, filters the junk out, asks how you want them sorted, saves to a txt.

**2. Resolve a list of domains**

Give it a file with one domain per line. It asks if u want just IPs or IP then the domain next to it. Resolves everything in parallel and writes it out.

**3. Both**

Finds subdomains, saves them, then asks if u actually wanna resolve them too. Default is no, so if you just wanted the list you can hit enter and bail.

## Output

Everything goes into a folder. default is `results`, but u can pick any name when it asks.

Example

```
results/
  subdomains.txt
  ips.txt
```

## Notes

- crt.name is the only source right now, no API key needed
- DNS resolution is threaded, up to 1000 workers
- Dead domains are counted but not written to the output file, only live ones land in there

## Requirements

Just requests, everything else is stdlib.

```
pip install requests
```

## Why

Got tired of doing this in three separate tools. now its one.
