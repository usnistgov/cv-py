__authors__ = ["Thurston"]
"""Modified from SpaCy in places"""

import requests
import os
import subprocess
import sys
from cv_py import __compatible__, __scispacy_version__
import argparse
import re
from pathlib import Path
import importlib
import pkg_resources
import dask.dataframe as dd
import requests
import semantic_version as sv

__all__ = ["load"]


def check_version():
    return False


def check_datapackage(datapackage):
    """check whether the zipped data package already exists"""
    path = f"{datapackage}-{__scispacy_version__}.tar.gz.dvc"
    is_file = os.path.isfile(path)
    if is_file and check_version() == __scispacy_version__:
        print("File is already up-to-date!")
        exit(0)
    elif is_file:
        return "update"
    else:
        return "import-url"

def check_dvc():
    """check whether or not dvc has been initiated in the current working directory (whether the .dvc config folder exists, more precisely)"""
    path = './.dvc'
    isdir = os.path.isdir(path)
    return isdir

def init_dvc():
    cmd = ["dvc", "init"]
    return subprocess.call(cmd, env=os.environ.copy())

def get_release_versions(proj_str):
    r = requests.get(f"https://api.github.com/repos/{proj_str}/tags").json()
    versions = [sv.Version(i["name"][1:]) for i in r if sv.validate(i["name"][1:])]
    return versions


def get_filename(datapackage="cord19_cdcs"):
    """get endpoint to download `datapackage`"""
    constraint = __compatible__.get(datapackage)
    assert (
        constraint is not None
    ), f"`{datapackage}` is not a supported datapackage name!"
    spec = sv.SimpleSpec(constraint)

    if datapackage == "cord19_cdcs":
        repo = "usnistgov/cord19-cdcs-nist"
        v = spec.select(get_release_versions(repo))
        fname = (
            f"https://github.com/{repo}/releases/download/v{v}/cord19-cdcs-{v}.tar.gz"
        )
        return fname
    else:
        fname = (
            f"https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v{__scispacy_version__}/{datapackage}-{__scispacy_version__}.tar.gz"
        )
        return fname

    # TODO other resources sources?



def download_datapackage(datapackage):
    download_url = get_filename(datapackage=datapackage)
    print(download_url)
    if not check_dvc():
        init_dvc()

    dvc_command = check_datapackage()
    cmd = ["dvc", dvc_command, datapackage]
    return subprocess.call(cmd, env=os.environ.copy())

def is_package(name):
    """Check if string maps to a package installed via pip.
    name (unicode): Name of package.
    RETURNS (bool): True if installed package, False if not.
    """
    name = name.lower()  # compare package name against lowercase name
    packages = pkg_resources.working_set.by_key.keys()
    for package in packages:
        if package.lower().replace("-", "_") == name:
            return True
    return False


def get_package_path(name):
    """Get the path to an installed package.
    name (unicode): Package name.
    RETURNS (Path): Path to installed package.
    """
    name = name.lower()  # use lowercase version to be safe
    # Here we're importing the module just to find it. This is worryingly
    # indirect, but it's otherwise very difficult to find the package.
    pkg = importlib.import_module(name)
    return Path(pkg.__file__).parent



def download_cli():

    parser = argparse.ArgumentParser(
        description="Helper to install CORD19 Datapackage locally for use by cv-py"
    )
    parser.add_argument(
        "--resource", "-r", type=str, help="Which resource to install?",
    )

    parser.add_argument(
        "--overwrite",
        dest="overwrite",
        action="store_true",
        help="whether to reinstall existing resource, if found",
    )
    parser.set_defaults(
        resource="cord19_cdcs", overwrite=False, pip_arg=None,
    )
    args = parser.parse_args()
    assert args.overwrite or not is_package(
        args.resource
    ), "Package already installed! To reinstall, pass `--overwrite`."

    download_datapackage(args.resource, user_pip_args=args.pip_arg)



def load(datapackage="cord19_cdcs", fmt="parquet"):
    """Return a python container (e.g. Dataframe) stored in `datapackage`.
    """
    assert is_package(datapackage), "Data Package must first be installed!"
    path_to_data = get_package_path(datapackage) / (datapackage + "." + fmt)

    return dd.read_parquet(
        path_to_data, engine="pyarrow"
    )  # TODO wrapper class or pattern match!


# pkg_resources.resource_filename('cord19_cdcs', 'cord19_cdcs.parquet')
