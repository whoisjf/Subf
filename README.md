# subf

Subdomain enumeration tool using [crt.name](https://crt.name).

I made this because [crt.sh](https://crt.sh) keeps throwing `503` errors for me, so this uses the `crt.name` API instead.

## Features

* Gets subdomains from certificate transparency data
* Removes exact duplicates
* Removes `www.` prefixes & saves unique domains only
* Filters out duplicate domains
* Keeps deeper subdomains
* Saves results to a `.txt` file

## Install

```bash
git clone https://github.com/whoisjf/Subf/
cd subf
pip3 install requests
```

## Usage

```bash
python3 subf.py
```

You'll be asked for the domain and output filename.

Leave the filename empty to save the results as `results.txt`.

## Note
Inspired by certificate transparency based subdomain enumeration tools.

Uses **crt.name** because **crt.sh** has been giving me `503 Service Unavailable` pretty often.
