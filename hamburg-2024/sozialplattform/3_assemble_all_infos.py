import json
from bs4 import BeautifulSoup


with open("data/1/kinderzuschlag.html", "r", encoding="utf-8") as file:
    html_data = file.read()

soup = BeautifulSoup(html_data, "html.parser")


def extract(element):
    formatted = ""
    for child in element.descendants:
        if child.name == "p":
            formatted += "\n" + child.get_text() + "\n"
        elif child.name == "li":
            formatted += "- " + child.get_text() + "\n"
    return formatted.strip()


pro = extract(soup.find(class_="bp-icon-box-paragraph__box pro"))
contra = extract(soup.find(class_="bp-icon-box-paragraph__box contra"))

print("pro:", pro)
print("contra:", contra)


with open("data/1/99107016017000.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)


def recursive(data, target_value):
    if isinstance(data, dict):
        for key, value in data.items():
            if value == target_value:
                val1 = BeautifulSoup(data["field_text"]["value"], "html.parser")
                val2 = BeautifulSoup(data["field_text_2"]["value"], "html.parser")  # can be null ?
                return extract(val1) + "\n" + extract(val2)
            result = recursive(value, target_value)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = recursive(item, target_value)
            if result is not None:
                return result
    return None

ret = recursive(json_data, "Habe ich Anspruch?")
print(ret)
