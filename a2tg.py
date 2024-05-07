#!/usr/bin/env python
"""
    Convert VSCode's .json themes and plain .css to Aard2's .css

    Created by Alexander Rusakevich
    Special thanks to @itkach for his Aard2!
"""

import os
import json
import datetime
import glob
import traceback
import pathlib
import sys
from colorama import Fore

from a2tg.download import download_themes
from a2tg.utils import *
from a2tg import __author__, __version__
from a2tg import *
from a2tg.convert_json import convert_json_to_aard2_css
from a2tg.convert_css import convert_css_to_aard2_css


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "download":
        download_themes()
        sys.exit(0)

    ignored_stems = [pathlib.Path(f).stem for f in json.load(
        open(os.path.join(".", "__ignore.json"), "r", encoding="utf8"))["ignore"]]

    if ignored_stems != []:
        print("Ignoring " + Fore.LIGHTYELLOW_EX + ", ".join(ignored_stems))

    json_files = [f for f in glob.glob(os.path.join(".", "src", "*.json"))
                  if not pathlib.Path(f).stem.startswith("__")
                  and pathlib.Path(f).stem not in ignored_stems]
    for json_file in json_files:
        print(f"Generating the theme for '{json_file}'...", end=" ")

        try:
            convert_json_to_aard2_css(json_file)
        except:
            print(Fore.LIGHTRED_EX + "Fail")
            print(traceback.format_exc())
        else:
            print(Fore.LIGHTGREEN_EX + "OK")

    css_files = [f for f in glob.glob(os.path.join(".", "src", "*.css"))
                 if not f.endswith(".aard2.css")
                 and pathlib.Path(f).stem not in ignored_stems]
    for css_file in css_files:
        print(f"Generating the theme for '{css_file}'...", end=" ")

        try:
            convert_css_to_aard2_css(css_file)
        except:
            print(Fore.LIGHTRED_EX + "Fail")
            print(traceback.format_exc())
        else:
            print(Fore.LIGHTGREEN_EX + "OK")


if __name__ == "__main__":
    main()
