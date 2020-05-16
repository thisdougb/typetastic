
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install

VERSION = "1.1.8"

with open("README.md", "r") as fh:
    long_description = fh.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)

setup(
    name="typetastic",
    version=VERSION,
    author="Doug Bridgens",
    author_email="typetastic@far-oeuf.com",
    keywords='automation screencast videotut',
    description="Python tool for building great screencasts, presentations, video tutorials..",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thisdougb/typetastic",
    project_urls={
        "Bug Tracker": "https://github.com/thisdougb/typetastic/issues",
        "Source Code": "https://github.com/thisdougb/typetastic",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Topic :: Education :: Computer Aided Instruction (CAI)"
    ],
    python_requires='>=3.6',
    install_requires=[
        'getch>=1.0',
        'pexpect>=4.8.0',
        'PyYAML>=5.3.1'
    ],
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
