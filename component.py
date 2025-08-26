import tempfile
import functools
import subprocess
from pathlib import Path

from kfp import dsl


pyproject = Path(__file__).parent / "pyproject.toml"


PIPELINE_COMPONENT_BASE_IMAGE = "python:3.12-slim"


def run(cmd: list[str]):
    try:
        subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e


def get_packages_to_install(group: str, pyproject: Path):
    """
    group: name of the dependency group
    pyproject: path to pyproject.toml where dependencies are specified

    Example: In this pyproject.toml the group="download_data"

    [dependency-groups]
    download-data = [
        "scikit-learn>=1.7.1"
    ]
    """
    print(f"Running uv export for {group}...")
    directory = pyproject.parent

    with tempfile.NamedTemporaryFile() as file:
        run(
            [
                "uv",
                "export",
                "--group",
                group,
                "--no-hashes",
                "--no-annotate",
                "--no-header",
                "--directory",
                str(directory),
                "--format",
                "requirements.txt",
                "-o",
                file.name,
            ]
        )
        packages = Path(file.name).read_text("utf-8").splitlines()
    return packages


@functools.wraps(dsl.component)
def custom_component(func, **kwargs):
    """
    A wrapper around kfp.dsl component that infers the dependencies based on the name
    the pipeline component.
    IMPORTANT: The dependencies group must have the exact same name as the component
    for it to work!
    """
    return dsl.component(
        func,
        base_image=PIPELINE_COMPONENT_BASE_IMAGE,
        packages_to_install=get_packages_to_install(func.__name__, pyproject=pyproject),
        **kwargs,
    )
