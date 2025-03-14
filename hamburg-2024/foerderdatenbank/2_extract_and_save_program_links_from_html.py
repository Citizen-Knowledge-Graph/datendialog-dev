import os
import json
from bs4 import BeautifulSoup


def get_program_links_from_file(file_path):
    links = []
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        soup = BeautifulSoup(content, "html.parser")

        # Find all the funding program divs
        program_divs = soup.find_all(
            "div", class_="card card--horizontal card--fundingprogram"
        )

        for div in program_divs:
            link = div.find("a", title="Öffnet die Einzelsicht")
            if link:
                href = link.get("href")
                links.append(href)

    return links


def scrape_all_links_from_folder(folder_path):
    all_links = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".html"):
            file_path = os.path.join(folder_path, file_name)
            links = get_program_links_from_file(file_path)
            all_links.extend(links)

    # deduplicate and sort the list
    all_links = sorted(list(set(all_links)))

    return all_links


# Folder containing the HTML files
folder_path = "html_files"

# Scrape all links from the folder
all_program_links = scrape_all_links_from_folder(folder_path)

# Save the links to a JSON file
output_file = "program_links.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(all_program_links, json_file, ensure_ascii=False, indent=4)

print(f"Scraped {len(all_program_links)} links and saved to {output_file}")
