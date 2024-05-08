import os


def fallback_get(dic: dict, *args: str) -> any:
    """Try to get element from dict using keys. If key 1 failed, try get by key 2 etc.

    :param dic: python dictionary structure
    :type dic: dict
    :raises Exception: None of the keys was found in dictionary
    :return: value in dict found
    :rtype: any
    """

    for arg in args:
        if arg in dic:
            return dic[arg]

    raise Exception(f"None of keys {args} was found in dictionary")


def gen_injection(inj_name: str) -> str:
    """Get injection (.css data) by injection name. Looks for .css files in config folder

    :param inj_name: css injection name
    :type inj_name: str
    :return: css data
    :rtype: str
    """

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
