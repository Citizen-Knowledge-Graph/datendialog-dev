import requests

# expects 00.csv in data/ars00 and the 2_distinct_ids.py script to be run before accordingly
# downloaded via https://public.demo.pvog.cloud-bdc.dataport.de/suchdienst/api/v5/servicedescriptions/csv?ars=00

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
    url = "https://public.demo.pvog.cloud-bdc.dataport.de/suchdienst/api/v5/servicedescriptions/000000000000/detail"
    count = 0
    with open("data/ars00/distinct_id-lbs.csv", mode="r") as file:
        for line in file:
            id = line.strip()
            filename = "data/ars00/vollstaendige_leistungsbeschreibungen/" + id + ".json"
            fetch_file(url, id, filename, count)
            count += 1
