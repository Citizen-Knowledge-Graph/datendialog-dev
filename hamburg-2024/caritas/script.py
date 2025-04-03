import requests
import json
import re
from bs4 import BeautifulSoup

def parse_item(item):
    contents_html = item.get("Contents", "")
    soup = BeautifulSoup(contents_html, "html.parser")

    street = None
    zipcode = None
    city = None
    phone = None
    email = None
    website = None

    address_div = soup.find("div", class_="venueGoogle")
    if address_div:
        text = address_div.get_text(separator="\n", strip=True)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if len(lines) >= 3:
            street = lines[0]
            zipcode = lines[1]
            city = lines[2]

    info_div = soup.find("div", class_="infoGoogle")
    if info_div:
        info_text = info_div.get_text("\n", strip=True)
        lines = [l.strip() for l in info_text.splitlines() if l.strip()]
        next_is_phone = False
        for l in lines:
            if next_is_phone:
                phone = l
                next_is_phone = False
            if l.lower().strip(":") == "fon":
                next_is_phone = True

        mail_link = info_div.find("a", href=re.compile(r"^mailto:"))
        if mail_link:
            email = mail_link["href"].replace("mailto:", "").strip()

        web_link = info_div.find("a", class_="ext-link")
        if web_link and web_link.get("href"):
            website = web_link["href"].strip()

    fields = {
        "ContentID": item.get("ContentID"),
        "Street": street,
        "Zipcode": zipcode,
        "City": city,
        "Phone": phone,
        "Email": email,
        "Website": website,
        "Latitude": item.get("Latitude"),
        "Longitude": item.get("Longitude"),
        "Title": (item.get("Title") or "").strip()
    }
    return { k: v for k, v in fields.items() if v is not None }


def fetch_all():
    base_url = "https://www.caritas.de/Services/MappingService.svc/GetMapContents/baad7256-65fe-423e-94f4-83de65b96151"
    params = {
        "datasource": "9a7d6fe2668948028233dbbbd46ef5f6",
        "page": 0,
        "pagesize": 10
    }
    all_items = []
    total_fetched = 0

    while True:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        items = data.get("Contents", [])
        for item in items:
            parsed = parse_item(item)
            all_items.append(parsed)
        #if len(all_items) > 1:
        #    break
        if not items:
            print("No more items to fetch")
            break
        total_fetched += len(items)
        print(f"Fetched so far: {total_fetched}")
        params["page"] += 1
    return all_items


if __name__ == "__main__":
    all_data = fetch_all()

    with open("sozialberatungsstellen.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_data)} items to sozialberatungsstellen.json")
    # two minor manual adjustments in the file: 2 " .de" and 3 ",  " fixed
