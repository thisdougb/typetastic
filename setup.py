import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="typetastic",
    version="1.1.2",
    author="Doug Bridgens",
    author_email="typetastic@far-oeuf.com",
    description="Python tool for building great screencasts, presentations, video tutorials..",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thisdougb/typetastic",
    project_urls={
        "Bug Tracker": "https://github.com/thisdougb/typetastic/issues",
        "Source Code": "https://github.com/thisdougb/typetastic",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Topic :: Education :: Computer Aided Instruction (CAI)"
    ],
    python_requires='>=3.6',
    install_requires=[
        'getch>=1.0',
        'pexpect>=4.8.0',
        'PyYAML>=5.3.1'
    ]
)
