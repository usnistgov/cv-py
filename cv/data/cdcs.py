__authors__ = ["Thurston"]
"""Modified from SpaCy in places"""

import requests
import os
import subprocess
import sys
from .. import about
import argparse
import re
from pathlib import Path
import importlib
import pkg_resources


__all__ = ['load']

alias = {
    'cord19-cdcs-nist':
        '/download/v{0}/cord19-cdcs-{0}.tar.gz'.format(about.__compatible__)
}

semver_regex = re.compile(  # Official
    r"(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))"
    r"?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?"
)


def get_filename(argument):
    fname = alias.get(argument)
    if not fname:
        try:
            ver = semver_regex.search(argument).group(0)
            fname = '/download/v{0}/cord19-cdcs-{0}.tar.gz'.format(ver)
        except AttributeError: raise
    return fname


def download():

    def _download_data(argument, user_pip_args=None):
        download_url = about.__download_url__ + get_filename(argument)
        print(download_url)
        pip_args = ["--no-cache-dir"]
        if user_pip_args:
            pip_args.extend(user_pip_args)
        cmd = [sys.executable, "-m", "pip", "install"] + pip_args + [download_url]
        return subprocess.call(cmd, env=os.environ.copy())

    parser = argparse.ArgumentParser(
        description="Helper to install CORD19 Datapackage locally for use by cv-py"
    )
    parser.add_argument("--datapackage", '-d',
                        default='cord19-cdcs-nist',
                        type=str,
                        help="Which data package to load?")
    args = parser.parse_args()

    _download_data(args.datapackage)  #TODO check if already installed


def load(datapackage='cord19_cdcs', format='parquet'):

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

    assert is_package(datapackage), "Data Package must first be installed!"
    path_to_data = get_package_path(datapackage)/(datapackage+'.' + format)

    import dask.dataframe as dd

    return dd.read_parquet(path_to_data)  #TODO wrapper class!

# pkg_resources.resource_filename('cord19_cdcs', 'cord19_cdcs.parquet')


