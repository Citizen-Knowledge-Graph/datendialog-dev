import os
import requests
import time

# Define the parameters with comments explaining each one
submit = "Suchen"
filter_categories = "FundingProgram"
# Set the search term here
template_query_string = "baum"

# Define the headers with comments explaining each one
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "cookie": "ROUTEID=.delivery2-replication; JSESSIONID=CE88420A12F6F83D70A3A34E83DD87CE.delivery2-replication",
    "dnt": "1",
    "priority": "u=0, i",
    "referer": "https://www.foerderdatenbank.de/SiteGlobals/FDB/Forms/Suche/Expertensuche_Formular.html?submit=Suchen&filterCategories=FundingProgram&templateQueryString=haushaltsmittel",
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}

# Base URL for the request
base_url = "https://www.foerderdatenbank.de/SiteGlobals/FDB/Forms/Suche/Expertensuche_Formular.html"


def save_html_files(response_text, folder_path, page_number):
    """Save the HTML response to a numbered HTML file in the specified folder."""
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Define file path
    html_file_path = os.path.join(folder_path, f"response_page_{page_number}.html")

    # Save the HTML response to an HTML file
    with open(html_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(response_text)

    print(f"Response successfully saved to {html_file_path}")


def main():
    folder_path = "html_files"
    page_number = 1
    previous_content = None

    while True:
        # Directly construct the URL for the current page
        gtp = f"%2526816beae2-d57e-4bdc-b55d-392bc1e17027_list%253D{page_number}"
        url = f"{base_url}?gtp={gtp}&submit={submit}&filterCategories={filter_categories}&templateQueryString={template_query_string}"

        try:
            # Make the API call
            response = requests.get(url, headers=headers)

            # Print the URL of the scraped page
            print(f"Scraped URL: {response.url}")

            # Check if the response was successful
            if response.status_code == 200:
                current_content = response.text.strip()

                # Check if the page is empty or contains no results
                if "Keine Treffer" in current_content or not current_content:
                    print(
                        f"No more search results. Stopping at page {page_number}. URL: {response.url}"
                    )
                    break

                # Check if the current page's content is the same as the previous page's content
                if current_content == previous_content:
                    print(
                        f"No more unique results. Stopping at page {page_number}. URL: {response.url}"
                    )
                    break

                # Save the current page's content
                save_html_files(current_content, folder_path, page_number)

                # Update the previous content
                previous_content = current_content
                page_number += 1

                # Pause for 1 second before the next request
                time.sleep(1)
            else:
                print(
                    f"Failed to fetch page {page_number}. Status code: {response.status_code}. URL: {response.url}"
                )
                break

        except Exception as e:
            print(
                f"Exception occurred on page {page_number}. URL: {response.url}. Error: {e}"
            )
            break


if __name__ == "__main__":
    main()
