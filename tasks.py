from invoke import run, task
from a2tg.download import download_themes
from a2tg.compile_themes import compile_themes
from a2tg import __version__
from colorama import Fore


@task
def download(context):
    download_themes()


@task
def compile(context):
    compile_themes()


@task
def pack(context):
    print(Fore.LIGHTGREEN_EX + "Packing...")

    dest_file = f"./dist/aard2-themes.tar.gz"
    run(f"tar -cvzf {dest_file} -C dist/themes .")

    print(
        Fore.LIGHTGREEN_EX
        + f".tar.gz with all themes ('{dest_file}') was created successfully"
    )


@task
def clear(context):
    run("rm -rvf dist build")
    run("pyclean .")


@task(pre=[download, compile, pack])
def build(context): ...
