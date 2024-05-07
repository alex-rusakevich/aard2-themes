aard2-themes
===

Download and unpack the latest archive from Releases section, then choose the theme file you fish in your `Aard2` app.

> All the themes are based on the `VSCode` themes, and none is created by myself *(read [__build.json](__build.json) if you want to know where the program downloads them from)*. I just convert them.

This repo does not include the original themes, if you want to compile the themes by yourself, install `python >= 3.9` and run:

```bash
# Prepare dependencies
pip install pipenv
pipenv install

# Compile themes
inv build
```
