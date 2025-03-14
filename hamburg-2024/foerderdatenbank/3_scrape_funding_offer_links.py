import requests
from bs4 import BeautifulSoup
import json


def scrape_url(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract text from a given CSS selector, handling cases where the selector finds no element
        def get_text_or_nan(selector):
            element = soup.select_one(selector)
            return " ".join(element.stripped_strings) if element else "nan"

        # Dictionary to hold the scraped data
        data = {
            "title": get_text_or_nan(".title"),
            "foerderart": get_text_or_nan(
                '.document-info-fundingprogram dt:contains("Förderart") + dd'
            ),
            "foerrderbereich": get_text_or_nan(
                '.document-info-fundingprogram dt:contains("Förderbereich") + dd'
            ),
            "foerrdergebiet": get_text_or_nan(
                '.document-info-fundingprogram dt:contains("Fördergebiet") + dd'
            ),
            "foerderberechtigte": get_text_or_nan(
                '.document-info-fundingprogram dt:contains("Förderberechtigte") + dd'
            ),
            "foerdergeber": get_text_or_nan(
                '.document-info-fundingprogram dt:contains("Fördergeber") + dd a'
            ),
            "ansprechpunkt_institution": get_text_or_nan(".card .card--title a"),
            "ansprechpunt_street": get_text_or_nan(".address .adr"),
            "ansprechpunkt_plz_ort": get_text_or_nan(".address .locality"),
            "ansprechpunkt_tel": get_text_or_nan(".person-contact .tel"),
            "ansprechpunkt_email": get_text_or_nan(".person-contact .email a"),
            "ansprechpunkt_url": get_text_or_nan(".person-contact .website a"),
            "weiterführende_links": get_text_or_nan(".document-info-item + dd a"),
            "kurztext": get_text_or_nan(".rich--text > h3:contains('Kurztext') + p"),
            "volltext": get_text_or_nan(
                ".rich--text > h3:contains('Volltext') + p, .rich--text > h3:contains('Volltext') + ul"
            ),
            "zusatzinfos": get_text_or_nan(
                "h2:contains('Zusatzinfos') + article .rich--text"
            ),
            "rechtsgrundlage": get_text_or_nan(
                "h2:has(span:contains('Rechtsgrundlage')) + article"
            ),
        }

        # Return the dictionary containing the scraped data
        return data

    except Exception as e:
        print(f"An error occurred while scraping {url}: {str(e)}")
        return None


def scrape_urls(url_list, base_url):
    all_data = []
    for partial_url in url_list:
        full_url = base_url + partial_url
        print(f"Scraping {full_url}")
        scraped_data = scrape_url(full_url)
        if scraped_data:
            all_data.append(scraped_data)
    return all_data


def main():
    # Load URLs from a JSON file
    with open("program_links.json", "r") as file:
        urls = json.load(file)

    base_url = "https://www.foerderdatenbank.de/"

    # Scrape the URLs and collect data
    scraped_data_list = scrape_urls(urls, base_url)

    # Save the scraped data to a JSON file
    with open("scraped_data.json", "w", encoding="utf-8") as outfile:
        json.dump(scraped_data_list, outfile, indent=4, ensure_ascii=False)

    print(f"Data scraped and saved for {len(scraped_data_list)} URLs.")


if __name__ == "__main__":
    main()
