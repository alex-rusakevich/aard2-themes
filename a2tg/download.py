import os
import json
import urllib3
import shutil
from http.client import responses
from colorama import Fore


def download_themes() -> None:
    print(Fore.LIGHTGREEN_EX + "The download has started!")

    metainf_file = json.load(open(os.path.join(
        ".", "__build.json"), "r", encoding="utf8"))

    download_queue = []

    for k, v in metainf_file.items():
        _, file_extension = os.path.splitext(v["download_link"])
        dest = os.path.join(".", "src", k + file_extension)
        download_queue.append((v["download_link"], dest))

    c = urllib3.PoolManager()

    for links in download_queue:
        print(
            f"Downloading '{os.path.split(links[1])[1]}' to ./src/...", end=" ")

        resp_status = None

        with c.request('GET', links[0], preload_content=False) as resp, open(links[1], 'wb') as out_file:
            shutil.copyfileobj(resp, out_file)
            resp_status = resp.status

        if int(resp_status) == 200:
            print(Fore.LIGHTGREEN_EX + "OK")
        else:
            print(Fore.LIGHTRED_EX + "Fail")
            print(f"HTTP {resp_status}: {responses[resp_status]}")