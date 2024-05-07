#!/usr/bin/env python
"""
    Convert VSCode's .json themes and plain .css to Aard2's .css

    Created by Alexander Rusakevich
    Special thanks to @itkach for his Aard2!
"""

import glob
import os
import pathlib
import sys
import traceback

from colorama import Fore

from a2tg import *
from a2tg import __author__, __version__
from a2tg.convert_css import convert_css_to_aard2_css
from a2tg.convert_json import convert_json_to_aard2_css
from a2tg.utils import *


def compile_themes():
    print(Fore.LIGHTGREEN_EX + "Compiling...")

    json_files = [
        f
        for f in glob.glob(os.path.join(THEMES_FOLDER, "*.json"))
        if not pathlib.Path(f).stem.startswith("__")
    ]

    css_files = [
        f
        for f in glob.glob(os.path.join(THEMES_FOLDER, "*.css"))
        if not f.endswith(".aard2.css")
    ]

    if not css_files and not json_files:
        print(Fore.LIGHTRED_EX + "No files to convert! Please, download them first")
        sys.exit(1)

    for json_file in json_files:
        print(f"Generating the theme for '{json_file}'...", end=" ")

        try:
            convert_json_to_aard2_css(json_file)
        except:
            print(Fore.LIGHTRED_EX + "Fail")
            print(traceback.format_exc())
        else:
            print(Fore.LIGHTGREEN_EX + "OK")

    for css_file in css_files:
        print(f"Generating the theme for '{css_file}'...", end=" ")

        try:
            convert_css_to_aard2_css(css_file)
        except:
            print(Fore.LIGHTRED_EX + "Fail")
            print(traceback.format_exc())
        else:
            print(Fore.LIGHTGREEN_EX + "OK")

    print(Fore.LIGHTGREEN_EX + "Done!")
