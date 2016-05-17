#!/usr/bin/python3

'''The setup and build script for the ayab library.'''

__author__ = 'AllYarnsAreBeautiful'
__version__ = '0.0.1'

import os
import sys

def read_file_named(file_name):
    here = os.path.dirname(__file__)
    file_path = os.path.join(here, file_name)
    with open(file_path) as f:
        return f.read()

# The base package metadata to be used by both distutils and setuptools
METADATA = dict(
    name = "ayab",
    version = __version__,
    packages = ['ayab'],
    author = __author__,
    author_email='niccokunzmann@rambler.ru',
    description='Python library for ayab knitting machines.',
    license='MIT',
    url='https://github.com/AllYarnsAreBeautiful/ayab',
    keywords='knitting ayab fashion',
)

# Run tests in setup
import setuptools.command.test

class PyTest(setuptools.command.test.test):
    # from https://github.com/j0057/setuptools-version-command/commit/527cd2aa289028a3cd6dc405ad2dd4e0d35f15bc
    # also look at https://github.com/pytest-dev/pytest/blob/master/setup.py
    def initialize_options(self):
        setuptools.command.test.test.initialize_options(self)

    def finalize_options(self):
        setuptools.command.test.test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # XXX: If I import pytest and call pytest.main, the setuptools_version_command module is already loaded, I think because
        # setuptools has it loaded as an entry_point. That means the top-level statements don't get executed while coverage is
        # watching, which means 16 missed statements. Reloading the module doesn't work, so the next best thing is to just run
        # the tests in a new process. However, it does mean that py.test has to be installed in either the system or the user's
        # site-packages.

        # import pytest
        # pytest.main()

        os.system('py.test')

# Extra package metadata to be used only if setuptools is installed
required_packages = [ package for package in
                        read_file_named("requirements.txt").splitlines()
                        if package ]
required_test_packages = [ package for package in
                             read_file_named("requirements-test.txt").splitlines()
                             if package ]
SETUPTOOLS_METADATA = dict(
    install_requires = required_packages,
    tests_require = required_test_packages,
    include_package_data = True,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        'tests': ['test_*.py'],
    },
    zip_safe = False,
    cmdclass={'test': PyTest},
)

def main():
    # Build the long_description from the README and CHANGES
    METADATA['long_description'] = read_file_named("README.rst")

    # Use setuptools if available, otherwise fallback and use distutils
    try:
        import setuptools
        METADATA.update(SETUPTOOLS_METADATA)
        setuptools.setup(**METADATA)
    except ImportError:
        import distutils.core
        distutils.core.setup(**METADATA)


if __name__ == '__main__':
    main()
