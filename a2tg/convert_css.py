import datetime
import json
import os
import pathlib

from a2tg import *
from a2tg import __author__, __version__
from a2tg.utils import *


def convert_css_to_aard2_css(file_name: str) -> None:
    theme_file_stem = pathlib.Path(file_name).stem
    css_theme_path = os.path.join(".", "themes", theme_file_stem + ".aard2.css")

    style_file = None
    with open(file_name, "r", encoding="utf8") as f:
        style_file = f.read().strip()

    metainf = json.load(open(os.path.join(".", "__build.json"), "r", encoding="utf8"))[
        theme_file_stem
    ]

    theme_name = theme_file_stem
    theme_type = "unknown"

    CSS_INJECTION = gen_injection(metainf["inject"])

    if "light" in theme_file_stem.lower() or "light" in theme_name.lower():
        theme_type = "light"
    elif "dark" in theme_file_stem.lower() or "dark" in theme_name.lower():
        theme_type = "dark"

    dt_now = str(datetime.datetime.utcnow())
    meta_repo = metainf["repo"]
    meta_author = metainf["author"]

    CSS_HEAD_ARGS = {
        "__author__": __author__,
        "__version__": __version__,
        "dt_now": dt_now,
        "theme_name": theme_name,
        "theme_type": theme_type,
        "meta_repo": meta_repo,
        "meta_author": meta_author,
    }

    CSS_HEAD = CSS_HEAD_BASE.format(**CSS_HEAD_ARGS)

    with open(css_theme_path, "w", encoding="utf8") as f:
        f.write(CSS_HEAD)

        if CSS_INJECTION:
            f.write("\n")
            f.write(CSS_INJECTION)

        f.write("\n\n")

        f.write(style_file)
        f.write("\n")
