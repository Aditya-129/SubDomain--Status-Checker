import requests
import sys
import os
import pyfiglet
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama
init(autoreset=True)

def main():
    # Print banner
    banner = pyfiglet.figlet_format("Subdomain Fuzzer")
    print(Fore.CYAN + banner)

    # Get user input
    wordlist_path = input("Enter path to wordlist file: ").strip()
    domain = input("Enter the target domain (e.g., example.com): ").strip()

    # Read wordlist
    try:
        with open(wordlist_path, "r") as f:
            subdomains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + "Wordlist file not found.")
        sys.exit(1)

    print(f"[*] Starting fuzzing for {len(subdomains)} subdomains on {domain}")

    # Prepare output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfilename = f"{domain}_{timestamp}.txt"
    active_subdomains = []

    for sub in subdomains:
        url = f"http://{sub}.{domain}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code < 400:
                print(Fore.GREEN + f"[+] Active: {url} -> {response.status_code}")
                active_subdomains.append(url)
            else:
                print(Fore.RED + f"[-] Dead: {url} -> {response.status_code}")
        except requests.RequestException:
            print(Fore.RED + f"[-] Dead: {url} (No response)")

    # Save active subdomains to file
    if active_subdomains:
        with open(outfilename, "w") as outf:
            for url in active_subdomains:
                outf.write(url + "\n")
        print(Fore.CYAN + f"\n[!] Active subdomains saved to {outfilename}")
    else:
        print(Fore.YELLOW + "\n[!] No active subdomains found.")

if __name__ == "__main__":
    main()
