__authors__ = ["Thurston"]
"""Modified from SpaCy in places"""

import requests
import os
import subprocess
import sys
from cv_py import __compatible__
import argparse
import re
from pathlib import Path
import importlib
import pkg_resources
import dask.dataframe as dd
import requests
import semantic_version as sv


__all__ = ["load"]


semver_regex = re.compile(  # Official
    r"(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))"
    r"?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?"
)


def get_release_versions(proj_url):
    r = requests.get(proj_url + "tags").json()
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
        dl_root = "https://github.com/usnistgov/cord19-cdcs-nist/"
        best_compatible = spec.select(get_release_versions(dl_root))
        fname = "download/v{0}/cord19-cdcs-{0}.tar.gz".format(best_compatible)
        return dl_root + fname
    else:  # TODO other data sources?
        raise NotImplementedError


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


def download_datapackage(datapackage, user_pip_args=None):
    download_url = get_filename(datapackage=datapackage)
    print(download_url)
    pip_args = ["--no-cache-dir"]
    if user_pip_args:
        pip_args.extend(user_pip_args)
    cmd = [sys.executable, "-m", "pip", "install"] + pip_args + [download_url]
    return subprocess.call(cmd, env=os.environ.copy())


def download_cli():

    parser = argparse.ArgumentParser(
        description="Helper to install CORD19 Datapackage locally for use by cv-py"
    )
    parser.add_argument(
        "--resource", "-r", type=str, help="Which resource to install?",
    )
    parser.add_argument(
        "--pip-arg",
        "-p",
        action="append",
        help="Argument to pass to pip (in addition to `--no-cache-dir`)",
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
