#!/usr/bin/env python3

import os
import sys
import requests
import json
from datetime import datetime
from googleapiclient.discovery import build
from screenshot import take_screenshot  # Assuming you have this from before

# === Configuration ===
API_KEY = "AIzaSyAf7oO6pgTBj9rXX5fuvYO7U9NAaGrxQmM"
CSE_ID = "6064e3c37e4384568"
ABSTRACT_API_KEY = "f34bf424c65f4bce954b3731c481adea"
NUMVERIFY_API_KEY = "b4b1b76d568510c3f75a2aff1bbff6fa"

PLATFORMS = {
    "Twitter": "https://twitter.com/{}",
    "GitHub": "https://github.com/{}",
    "Instagram": "https://instagram.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Facebook": "https://www.facebook.com/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Medium": "https://medium.com/@{}",
    "Vimeo": "https://vimeo.com/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Roblox": "https://www.roblox.com/user.aspx?username={}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "Ko-fi": "https://ko-fi.com/{}"
}

def generate_usernames(first, last):
    first = first.lower()
    last = last.lower()
    return list(set([
        f"{first}{last}", f"{last}{first}", f"{first}.{last}", f"{first}_{last}",
        f"{first[0]}{last}", f"{first}{last[0]}", f"{first}{last}123",
        f"{first}{last}01", f"{first}_{last}01", f"{first[0]}{last}01",
        f"{first}{last[0]}01", f"{first}", f"{last}", f"{first}.{last[0]}",
        f"{first}{last[0]}123"
    ]))

def check_profiles(usernames):
    found_profiles = []
    headers = {"User-Agent": "Mozilla/5.0 (compatible; OSINT-Tool/1.0)"}
    for username in usernames:
        for platform, url_template in PLATFORMS.items():
            url = url_template.format(username)
            try:
                r = requests.get(url, headers=headers, timeout=5)
                if r.status_code == 200:
                    print(f"[+] Found {platform} profile: {url}")
                    found_profiles.append({"platform": platform, "username": username, "url": url})
                    take_screenshot(url, f"{platform}_{username}.png")  # save screenshot
                else:
                    print(f"[-] No {platform} profile: {username}")
            except requests.RequestException:
                print(f"[!] Error checking {url}")
    return found_profiles

def google_search(api_key, cse_id, query, num=10):
    print(f"[*] Searching Google for: {query}")
    service = build("customsearch", "v1", developerKey=api_key)
    try:
        res = service.cse().list(q=query, cx=cse_id, num=num).execute()
        results = []
        for item in res.get('items', []):
            results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            })
        print(f"[+] Found {len(results)} Google search results")
        return results
    except Exception as e:
        print(f"[!] Google search error: {e}")
        return []

def lookup_email(email):
    try:
        url = f"https://emailvalidation.abstractapi.com/v1/?api_key={ABSTRACT_API_KEY}&email={email}"
        r = requests.get(url)
        return r.json() if r.status_code == 200 else {}
    except:
        return {}

def lookup_phone(phone):
    try:
        url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={phone}"
        r = requests.get(url)
        return r.json() if r.status_code == 200 else {}
    except:
        return {}

def save_results(data, first, last):
    os.makedirs("results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join("results", f"{first}_{last}_osint_{timestamp}.json")
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[+] Results saved to: {output_file}")

def run_osint(first, last, email=None, phone=None):
    usernames = generate_usernames(first, last)
    print(f"[*] Generated usernames: {usernames}")

    profiles = check_profiles(usernames)
    google_results = google_search(API_KEY, CSE_ID, f"{first} {last}")

    enrichment = {}
    if email:
        enrichment["email_info"] = lookup_email(email)
    if phone:
        enrichment["phone_info"] = lookup_phone(phone)

    data = {
        "input": {
            "first": first,
            "last": last,
            "usernames_checked": usernames,
            "email": email,
            "phone": phone
        },
        "profiles_found": profiles,
        "google_results": google_results,
        "enrichment": enrichment,
        "timestamp": datetime.now().isoformat()
    }

    save_results(data, first, last)

# Only runs when used from terminal
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 osint_tool.py Firstname Lastname [email] [phone]")
        sys.exit(1)

    first = sys.argv[1]
    last = sys.argv[2]
    email = sys.argv[3] if len(sys.argv) > 3 else None
    phone = sys.argv[4] if len(sys.argv) > 4 else None

    run_osint(first, last, email, phone)

