# uses the sdsu.csv to get the org ids and the websites of the clubs to then 
# scrape for instagram accounts, if found take that and put the profile picture 
# in media/club_logos
# if not found, use the website to scrape for the logo 

import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin
import os
from tqdm import tqdm

# convoluted lmaooo 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) # essentailly the root,
# hackathon-426/hackathon_426

SDSU_CLUBS_CSV = os.path.join(BASE_DIR, "sdsu_clubs.csv")
NO_LOGOS_CSV = os.path.join(BASE_DIR, "sdsu_clubs_no_logos.csv")
LOGO_DIR = os.path.join(BASE_DIR, "media", "club_logos")



os.makedirs(LOGO_DIR, exist_ok=True)

def download_logo(logo_url, save_path):
    try:
        response = requests.get(logo_url, timeout=5)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded logo to {save_path}")
        else:
            print(f"Failed to download logo: {response.status_code}")
    except Exception as e:
        print(f"Error downloading logo: {e}")
        
def find_instagram(website_url):
    try:
        response = requests.get(website_url, timeout=5)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        # Look for Instagram links in the website
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and "instagram.com" in href:
                return href.split("?")[0]  # Remove any query parameters
        return None
    except Exception as e:
        print(f"Error finding Instagram: {e}")
        return None
    
def get_instagram_pfp(instagram_url):
    try:
        response = requests.get(instagram_url, timeout=5)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        # Find the profile picture URL in the HTML
        profile_pic = soup.find("img", {"alt": "Profile picture"})
        if profile_pic:
            return profile_pic.get("src")
        return None
    except Exception as e:
        print(f"Error getting Instagram profile picture: {e}")
        return None
    
def get_website_logo(website_url):
    try:
        response = requests.get(website_url, timeout=5)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        # Look for common logo image tags
        logo_tags = ["img", "link"]
        for tag in logo_tags:
            for img in soup.find_all(tag):
                if tag == "img":
                    src = img.get("src")
                else:
                    src = img.get("href")
                if src and (".png" in src or ".jpg" in src or ".jpeg" in src):
                    return urljoin(website_url, src)  # Make the URL absolute
        return None
    except Exception as e:
        print(f"Error getting website logo: {e}")
        return None
    
def main():
    # make a new csv file to store the websites without logos, so that it's easier to add them later on 
    # to keep it basic, just need the name of the club and a supposed website and org id probably
    
    
    with open(NO_LOGOS_CSV, mode="w", newline="", encoding='utf-8') as file:
        missing_writer = csv.DictWriter(file, fieldnames=["Name", "Website", "ID"])
        missing_writer.writeheader()
    
    rows = []
    with open(SDSU_CLUBS_CSV, newline="", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in tqdm(reader, desc="finding instagram links", unit="club"):
            website = row.get("Website")
            instagram_url = find_instagram(website) if website else None
            row["Instagram"] = instagram_url or ""
            rows.append(row)
            time.sleep(1)
            
    # update csv 
    fieldnames = list(rows[0].keys())
    with open(SDSU_CLUBS_CSV, mode="w", newline="", encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print ("Instagram links added to CSV")
    
    for row in tqdm(rows, desc="Downloading logos", unit="club"):
        club_name = row['Name'].replace("/", "_").replace(" ", "_")
        instagram_url = row.get("Instagram")
        website_url = row.get("Website")
        
        logo_save_path = os.path.join(LOGO_DIR, f"{club_name}.jpg")
        
        if instagram_url:
            pfp_url = get_instagram_pfp(instagram_url)
            if pfp_url:
                download_logo(pfp_url, logo_save_path)
        
        elif website_url:
            logo_url = get_website_logo(website_url)
            if logo_url:
                download_logo(logo_url, logo_save_path)
            else:
                print(f"No logo found for {club_name} on website")
        else:
            # No Instagram or website found then add it to a new csv file 
            with open(NO_LOGOS_CSV, mode="a", newline="", encoding='utf-8') as file:
                missing_writer = csv.DictWriter(file, fieldnames=["Name", "Website", "ID"])
                missing_writer.writerow({
                    "Name": club_name,
                    "Website": website_url,
                    "ID": row.get("ID")
                })  

        if not instagram_url and not website_url:
            # If neither Instagram nor website is available, log the club name
            print(f"No Instagram or website for {club_name}")
        time.sleep(1) 
        
if __name__ == "__main__":
    main()
    
    
            