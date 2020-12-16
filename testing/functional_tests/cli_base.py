import sys
import os
import shutil
from ivadomed.utils import init_ivadomed, __ivadomed_dir__
from ivadomed.scripts import download_data as ivadomed_download_data

__test_dir__ = os.path.join(__ivadomed_dir__, 'testing/functional_tests')
__fixtures_dir__ = os.path.join(__test_dir__, 'fixtures')
__tmp_dir__ = os.path.join(__test_dir__, "tmp")
sys.path.append(__test_dir__)

init_ivadomed()


class bcolors(object):
    normal = '\033[0m'
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    magenta = '\033[95m'
    cyan = '\033[96m'
    bold = '\033[1m'
    underline = '\033[4m'


def printv(string, verbose=1, type='normal'):
    """Enables to print color-coded messages, depending on verbose status.
    Only use in command-line programs (e.g. sct_propseg).
    """

    colors = {
        'normal': bcolors.normal,
        'info': bcolors.green,
        'warning': bcolors.yellow,
        'error': bcolors.red,
        'code': bcolors.blue,
        'bold': bcolors.bold,
        'process': bcolors.magenta
    }

    if verbose:
        # The try/except is there in case stdout does not have isatty field (it did happen to me)
        try:
            # Print color only if the output is the terminal
            if sys.stdout.isatty():
                color = colors.get(type, bcolors.normal)
                print(color + string + bcolors.normal)
            else:
                print(string)
        except Exception:
            print(string)


def download_dataset(dataset='data_testing', verbose=True):
    """Download testing data from internet.

    Args:
        verbose (bool): whether or not to print
    """
    printv('\nDownloading testing data...', verbose)
    __dataset_dir__ = os.path.join(__test_dir__, dataset)
    ivadomed_download_data.main([
        '-d', dataset,
        '-o', __dataset_dir__
    ])


def remove_dataset(dataset='data_testing', verbose=True):
    """Recursively remove the data_testing folder.

    Args:
        verbose (bool): whether or not to print
    """
    __dataset_dir__ = os.path.join(__test_dir__, dataset)
    printv("rm -rf %s" % (__dataset_dir__), verbose=verbose, type="code")
    shutil.rmtree(__dataset_dir__, ignore_errors=True)


def create_tmp_dir():
    """Create temporary directory for test data.

    This directory copies the ``fixtures`` directory to a ``tmp`` directory.
    Any data files created during testing will go into ``tmp`` directory.
    This is created/removed for each test.
    """
    remove_tmp_dir()
    shutil.copytree(__fixtures_dir__, __tmp_dir__)


def remove_tmp_dir():
    """Recursively remove the ``tmp`` directory if it exists.
    """
    shutil.rmtree(__tmp_dir__, ignore_errors=True)