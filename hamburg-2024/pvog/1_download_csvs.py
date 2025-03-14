import requests


def fetch_csv(url, ars, filename, count):
    try:
        print(f"{count}: fetching CSV for ARS: {ars}")
        response = requests.get(url, params={"ars": ars})
        response.raise_for_status()

        with open(filename, "wb") as file:
            file.write(response.content)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    url = "https://public.demo.pvog.cloud-bdc.dataport.de/suchdienst/api/v5/servicedescriptions/csv"
    count = 0
    with open("data/0/ars.csv", mode="r") as file:
        for line in file:
            ars = line.strip()
            filename = "data/1/" + ars + ".csv"
            fetch_csv(url, ars, filename, count)
            count += 1
