import os
import json
import datetime
import re
import pathlib
import jsonstrip

from a2tg.utils import *
from a2tg import *
from a2tg import __version__, __author__


def convert_json_to_aard2_css(file_name: str) -> None:
    theme_file_stem = pathlib.Path(file_name).stem
    css_theme_path = os.path.join(
        ".", "themes", theme_file_stem + ".aard2.css")

    style_file = None
    with open(file_name, "r", encoding="utf8") as file:
        style_file = json.loads(jsonstrip.strip(file.read()))

    metainf = json.load(open(os.path.join(
        ".", "__build.json"), "r", encoding="utf8"))[theme_file_stem]

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
    CSS_INJECTION = gen_injection(metainf["inject"])

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

        f.write("\n")
        f.write(CSS_INJECTION)
        f.write("\n\n")

        css_theme_code = CSS_BASE

        for k, v in colors.items():
            css_theme_code = re.sub(fr"\${k}(?=\W)", v, css_theme_code)

        f.write(css_theme_code.strip())
        f.write("\n")