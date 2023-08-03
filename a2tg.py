#!/usr/bin/env python
"""
    Convert VSCode's .json themes to Aard2's .css
"""

__author__ = "Alexander Rusakevich"
__version_arr__ = (0, 0, 5)
__version__ = "v" + ".".join([str(i) for i in __version_arr__])

import os
import json
import datetime
import glob
import colorama
import re
import traceback
import pathlib
from colorama import Fore

colors = {
    "bg_color": "black",
    "font_color": "#a0a0a0",

    "a_color": "#a3964e",
    "a_color_active": "#faa700",
    "a_color_visited": "#735a0a",

    "tr_color": "orangered",
    "pos_color": "green",
    "co_color": "#888888"
}

CSS_BASE = open("base_theme.scss", "r", encoding="utf8").read()

CSS_HEAD_BASE = """
/* 
 * Generated by Aard2 theme generator {__version__} (created by {__author__})
 * {dt_now}
 *
 * Theme: {theme_name}
 * Type: {theme_type}
 *
 * Original author of the theme: {meta_author}
 * Repo: {meta_repo}
 * 
 * Special thanks to @itkach for his Aard2!
 */
""".strip() + (2*"\n")


def fallback_get(dic, *args):
    for arg in args:
        if arg in dic:
            return dic[arg]

    return None


def convert_json_to_aard2_css(file_name: str) -> None:
    theme_file_stem = pathlib.Path(file_name).stem
    css_theme_path = os.path.join(
        ".", "themes", theme_file_stem + ".aard2.css")

    style_file = None
    with open(file_name, "r", encoding="utf8") as f:
        style_file = json.load(f)

    metainf = json.load(open(os.path.join(
        ".", "__metainf.json"), "r", encoding="utf8"))[theme_file_stem]

    theme_name = style_file.get("name", theme_file_stem)
    theme_type = style_file.get("type", "unknown")

    if theme_type == "unknown":
        if "light" in theme_file_stem.lower() or "light" in theme_name.lower():
            theme_type = "light"
        elif "dark" in theme_file_stem.lower() or "dark" in theme_name.lower():
            theme_type = "dark"

    dt_now = str(datetime.datetime.utcnow())
    meta_repo = metainf["repo"]
    meta_author = metainf["author"]

    CSS_HEAD_ARGS = {
        "__author__": __author__, "__version__": __version__,
        "dt_now": dt_now, "theme_name": theme_name,
        "theme_type": theme_type, "meta_repo": meta_repo,
        "meta_author": meta_author
    }

    CSS_HEAD = CSS_HEAD_BASE.format(**CSS_HEAD_ARGS)

    file_colors = style_file["colors"]

    colors["bg_color"] = file_colors["editor.background"]
    colors["font_color"] = file_colors["editor.foreground"]

    colors["a_color"] = fallback_get(
        file_colors, "textLink.foreground", "inputValidation.infoBorder", "terminal.ansiCyan")
    colors["a_color_active"] = fallback_get(
        file_colors, "textLink.activeForeground", "inputValidation.infoBackground", "terminal.ansiBlue")
    colors["a_color_visited"] = fallback_get(
        file_colors, "inputValidation.errorBackground", "terminal.ansiBrightMagenta")

    colors["tr_color"] = file_colors["terminal.ansiYellow"]
    colors["pos_color"] = file_colors["terminal.ansiGreen"]
    colors["co_color"] = file_colors["terminal.ansiBrightBlack"]

    for k, v in colors.items():
        if v == None:
            raise SyntaxError(
                f"Cannot find color for {k} in '{file_name}'. Please, check this theme or use another one")

    with open(css_theme_path, "w", encoding="utf8") as f:
        f.write(CSS_HEAD)

        css_theme_code = CSS_BASE

        for k, v in colors.items():
            css_theme_code = re.sub(fr"\${k}(?=\W)", v, css_theme_code)

        f.write(css_theme_code)


def convert_css_to_aard2_css(file_name: str) -> None:
    theme_file_stem = pathlib.Path(file_name).stem
    css_theme_path = os.path.join(
        ".", "themes", theme_file_stem + ".aard2.css")

    style_file = None
    with open(file_name, "r", encoding="utf8") as f:
        style_file = f.read().strip()

    metainf = json.load(open(os.path.join(
        ".", "__metainf.json"), "r", encoding="utf8"))[theme_file_stem]

    theme_name = theme_file_stem
    theme_type = "unknown"

    if "light" in theme_file_stem.lower() or "light" in theme_name.lower():
        theme_type = "light"
    elif "dark" in theme_file_stem.lower() or "dark" in theme_name.lower():
        theme_type = "dark"

    dt_now = str(datetime.datetime.utcnow())
    meta_repo = metainf["repo"]
    meta_author = metainf["author"]

    CSS_HEAD_ARGS = {
        "__author__": __author__, "__version__": __version__,
        "dt_now": dt_now, "theme_name": theme_name,
        "theme_type": theme_type, "meta_repo": meta_repo,
        "meta_author": meta_author
    }

    CSS_HEAD = CSS_HEAD_BASE.format(**CSS_HEAD_ARGS)

    with open(css_theme_path, "w", encoding="utf8") as f:
        f.write(CSS_HEAD)
        f.write(style_file)
        f.write("\n")


def main():
    colorama.init(autoreset=True)

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
