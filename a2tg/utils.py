import os


def fallback_get(dic, *args):
    for arg in args:
        if arg in dic:
            return dic[arg]

    return None


def gen_injection(inj_name) -> str:
    if not inj_name:
        return ""

    real_inj_name = inj_name + ".css"
    css_inj_title = f"/* ========= {real_inj_name} ========= */"

    inj = (
        css_inj_title
        + "\n"
        + (
            open(
                os.path.join(".", "config", inj_name + ".css"),
                "r",
                encoding="utf8",
            )
            .read()
            .strip()
            if inj_name
            else ""
        )
    )

    return inj + "\n" + f"/* {'=' * (len(css_inj_title) - 6)} */"
