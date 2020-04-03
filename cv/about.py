from os.path import dirname, isdir, join
from pathlib import Path
import re
from subprocess import CalledProcessError, check_output

# Source: https://github.com/Changaco/version.py
PREFIX = 'v'
tag_re = re.compile(r'\btag: %s([0-9][^,]*)\b' % PREFIX)
version_re = re.compile('^Version: (.+)$', re.M)


def get_version():
    # Return the version if it has been injected into the file by git-archive
    version = tag_re.search('$Format:%D$')
    if version:
        return version.group(1)

    d = Path(__file__)

    if (d.parents[1]/'.git').exists():
        # Get the version using "git describe".
        cmd = 'git describe --tags --match %s[0-9]* --dirty' % PREFIX
        try:
            version = check_output(cmd.split()).decode().strip()[len(PREFIX):]
        except CalledProcessError:
            raise RuntimeError('Unable to get version number from git tags')

        # PEP 440 compatibility
        if '-' in version:
            if version.endswith('-dirty'):
                # raise RuntimeError('The working tree is dirty')
                version = version[:-len('-dirty')]  # ignore it
                import warnings
                warnings.warn('The working tree is dirty!')
            print(version)
            version = '.r'.join(version.split('-')[:2])

    else:
        # Extract the version from the PKG-INFO file.
        with (d.parents[1]/'PKG-INFO').open() as f:
            version = version_re.search(f.read()).group(1)
    return version


__title__ = "cv-py"
# __version__ = get_version() # TODO
__version__ = "0.1.0"
__compatible__ = "0.1.1"
__release__ = False
__download_url__ = "https://github.com/usnistgov/cord19-cdcs-nist/releases"


if __name__ == '__main__':
    print(get_version())