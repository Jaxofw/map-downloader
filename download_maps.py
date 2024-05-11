import os
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

fastdl_url = "https://iswenzz.com/static/fastdl/usermaps/"


def main():
    maps = get_links(fastdl_url)

    if len(maps) == 0:
        print("No maps found")
        return

    for map in maps:
        map = map["href"]

        if is_map_downloaded(map) or not is_dr_map(map):
            continue

        # Remove trailing slash
        map = map[0 : len(map) - 1]

        # Create the directory for the map if it doesn't exist
        os.makedirs(f"usermaps/{map}", exist_ok=True)

        map_files = get_links(fastdl_url + map)

        print(f"Downloading {map}")

        for file in map_files:
            file = file["href"]

            if is_map_file(file):
                download_file(map, file)

    print("Done")


def get_links(url):
    try:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all("a")
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def download_file(map, file):
    with open(f"usermaps/{map}/{file}", "wb") as map_file:
        content = requests.get(fastdl_url + map + "/" + file, verify=False).content
        map_file.write(content)


def is_map_downloaded(map_name):
    return os.path.exists(f"usermaps/{map_name}")


def is_dr_map(map):
    return map.startswith("mp_deathrun_") or map.startswith("mp_dr_")


def is_map_file(file):
    return file.endswith(".ff") or file.endswith(".iwd")


main()
