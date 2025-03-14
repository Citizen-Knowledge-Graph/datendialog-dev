import requests

url = "https://sozialplattform.de/content/de/api/v1/node/leika_service"

response = requests.get(url)
json = response.json()

for item in json["data"]:
    breadcrumbs = item["attributes"]["bp_breadcrumbs"]
    if len(breadcrumbs) > 1:
        second_breadcrumb = breadcrumbs[1]  # for bildung und teilhabe its in the 3rd TODO
        alias = second_breadcrumb.get("alias")
        leikaId = second_breadcrumb.get("fieldVsmLeistungId")
        print(leikaId, alias)
