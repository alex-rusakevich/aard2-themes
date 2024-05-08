aard2-themes
===

Download and unpack the latest `aard2-themes.tar.gz` archive from *Releases* section, then choose any `.aard2.css` theme file you wish in your `Aard2` app.

> All the themes are based on the `VSCode` themes, and none is created by myself *(read [the build targets file](config/build_targets.json) if you want to know where the program downloads them from)*. I just convert them to `.aard2.css`.

This repo does not include the original themes, if you want to compile the themes by yourself, install `python >= 3.9` and run:

```bash
# Prepare dependencies
pip install pipenv
pipenv install

# Compile themes
inv build
```
