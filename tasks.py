from invoke import run, task


@task
def download(context): ...


@task
def compile_themes(context): ...


@task
def pack(context): ...


@task(pre=[download, compile_themes, pack])
def build(context): ...
