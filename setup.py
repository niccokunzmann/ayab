#!/usr/bin/python3

'''The setup and build script for the ayab library.'''

import os
import sys
from setuptools.command.test import test as TestCommandBase

__author__ = 'AllYarnsAreBeautiful'
here = os.path.dirname(__file__)
sys.path.insert(0, here)
from ayab import __version__

def read_file_named(file_name):
    file_path = os.path.join(here, file_name)
    with open(file_path) as f:
        return f.read()

def read_filled_lines_from_file_named(file_name):
    content = read_file_named("requirements-test.txt")
    lines = content.splitlines()
    return [line for line in lines if line]

# The base package metadata to be used by both distutils and setuptools
METADATA = dict(
    name="ayab",
    version=__version__,
    packages=['ayab'],
    author=__author__,
    author_email='niccokunzmann@rambler.ru',
    description='Python library for ayab knitting machines.',
    license='MIT',
    url='https://github.com/AllYarnsAreBeautiful/ayab',
    keywords='knitting ayab fashion',
)

# Run tests in setup


class TestCommand(TestCommandBase):

    TEST_ARGS = []

    def finalize_options(self):
        TestCommandBase.finalize_options(self)
        self.test_suite = True
        self.test_args = self.TEST_ARGS

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


class CoverageTestCommand(TestCommand):
    TEST_ARGS = ["--cov=ayab"]

class FlakesTestCommand(TestCommand):
    TEST_ARGS = ["--flakes"]

class FlakesCommand(TestCommand):
    TEST_ARGS = ["--flakes", "-m", "flakes"]

class CoverageFlakesTestCommand(TestCommand):
    TEST_ARGS = ["--cov=ayab", "--flakes"]

# Extra package metadata to be used only if setuptools is installed
required_packages = \
    read_filled_lines_from_file_named("requirements.txt")
required_test_packages = \
    read_filled_lines_from_file_named("requirements-test.txt")

SETUPTOOLS_METADATA = dict(
    install_requires=required_packages,
    tests_require=required_test_packages,
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    package_data=dict(
        # If any package contains of these files, include them:
        tests=['test_*.py'],
    ),
    zip_safe=False,
    cmdclass={
        "test":TestCommand,
        "coverage_test":CoverageTestCommand,
        "flakes":FlakesCommand,
        "flakes_test":FlakesTestCommand,
        "coverage_flakes_test":CoverageFlakesTestCommand,
        },
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
