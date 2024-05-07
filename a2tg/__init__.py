__author__ = "Alexander Rusakevich"
__version_arr__ = (1, 1)
__version__ = "v" + ".".join([str(i) for i in __version_arr__])

import colorama
import pathlib

colorama.init(autoreset=True)

RESULT_THEMES_FOLDER = pathlib.Path(".", "dist", "themes")
RESULT_THEMES_FOLDER.mkdir(parents=True, exist_ok=True)

THEMES_FOLDER = pathlib.Path(".", "build")
THEMES_FOLDER.mkdir(parents=True, exist_ok=True)

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
""".strip() + (
    "\n"
)


colors = {
    "bg_color": "black",
    "font_color": "#a0a0a0",
    "a_color": "#a3964e",
    "a_color_active": "#faa700",
    "a_color_visited": "#735a0a",
    "tr_color": "orangered",
    "pos_color": "green",
    "co_color": "#888888",
}
