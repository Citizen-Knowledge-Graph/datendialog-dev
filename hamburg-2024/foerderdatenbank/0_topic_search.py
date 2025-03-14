import requests
import json
from itertools import product
import string
import time
import os


def generate_search_terms(min_length, max_length):
    alphabet = string.ascii_lowercase
    return [
        "".join(term)
        for length in range(min_length, max_length + 1)
        for term in product(alphabet, repeat=length)
    ]


def fetch_suggestions(term):
    url = "https://www.foerderdatenbank.de/SiteGlobals/FDB/Forms/Suche/Servicesuche_Autosuggest_Formular.json"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": "ROUTEID=.delivery2-replication; JSESSIONID=ADD765CF639C7A22CF1C69084A1F9FD7.delivery2-replication",
        "dnt": "1",
        "referer": "https://www.foerderdatenbank.de/SiteGlobals/FDB/Forms/Suche/Startseitensuche_Formular.html",
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }
    params = {"userQuery": term}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def append_to_json_file(filename, new_data):
    if not os.path.isfile(filename):
        # If file does not exist, create it and write the new data as a list
        with open(filename, 'w') as f:
            json.dump([new_data], f, ensure_ascii=False, indent=4)
    else:
        # If file exists, read the existing data, append the new data, and write it back
        with open(filename, 'r') as f:
            data = json.load(f)
        data.append(new_data)
        with open(filename, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    min_length = 2
    max_length = 4
    search_terms = generate_search_terms(min_length, max_length)
    results = []

    print(f"Generated {len(search_terms):,} search terms.")
    print(f"Estimated time to complete: {len(search_terms) / 60 / 60:,.2f} hours.")

    for i, term in enumerate(search_terms):
        try:
            suggestions = fetch_suggestions(term)
            if suggestions["suggestions"]:  # Checking if suggestions are not empty
                for item in suggestions["suggestions"]:
                    results.append({"name": item["name"], "count": item["count"]})
            time.sleep(1)  # Pause for 1 second to avoid hitting the API too hard
        except requests.HTTPError as e:
            print(f"Failed to fetch suggestions for '{term}': {e}")
        except KeyError:
            print(f"No suggestions found for '{term}'.")

        # append intermediate results
        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1} search terms. Saving intermediate results.")
            append_to_json_file("suggestions.json", results)


if __name__ == "__main__":
    main()
