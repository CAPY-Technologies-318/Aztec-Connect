import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://stuapp.sdsu.edu/RSO/search/Detail?OrgID={}"
OUTPUT_FILE = "sdsu_clubs.csv"

def extract_text_or_none(soup, header_id):
    td = soup.find("td", {"headers": header_id})
    return td.get_text(strip=True).replace('\n', ' ') if td else None

def extract_website(soup):
    td = soup.find("td", {"headers": "website"})
    if td:
        link = td.find("a")
        return link.get("href") if link else None
    return None

def scrape_org(org_id):
    url = BASE_URL.format(org_id)
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")

        org_name = extract_text_or_none(soup, "orgname")
        if not org_name:
            return None  # skip invalid entries

        return {
            "ID": org_id,
            "Name": org_name,
            "Type": extract_text_or_none(soup, "orgtype"),
            "Website": extract_website(soup),
            "Purpose": extract_text_or_none(soup, "purpose"),
            "Meeting Day": extract_text_or_none(soup, "meetday"),
            "Meeting Location": extract_text_or_none(soup, "meetloc"),
        }

    except Exception as e:
        print(f"Error with ID {org_id}: {e}")
        return None

def main():
    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["ID", "Name", "Type", "Website", "Purpose", "Meeting Day", "Meeting Location"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for org_id in range(0, 10001):
            print(f"Scraping Org ID: {org_id}")
            data = scrape_org(org_id)
            if data:
                writer.writerow(data)

if __name__ == "__main__":
    main()
