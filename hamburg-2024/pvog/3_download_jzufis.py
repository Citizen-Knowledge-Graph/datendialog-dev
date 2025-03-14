import requests


def fetch_file(url, id, filename, count):
    try:
        print(f"{count}: fetching JSON for ID: {id}")
        response = requests.get(url, params={"q": id})
        response.raise_for_status()

        with open(filename, "wb") as file:
            file.write(response.content)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    url = "https://public.demo.pvog.cloud-bdc.dataport.de/suchdienst/api/v2/servicedescriptions/jzufi"
    count = 0
    with open("data/2/distinct_id-lbs.csv", mode="r") as file:
        for line in file:
            id = line.strip()
            filename = "data/3/" + id + ".json"
            fetch_file(url, id, filename, count)
            count += 1
