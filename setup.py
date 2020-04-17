import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="typetastic",
    version="0.0.1",
    author="Doug Bridgens",
    author_email="typetastic@far-oeuf.com",
    description="Python utility to make recording screencasts easier.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thisdougb/typetastic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pexpect>=4.8.0',
        'PyYAML>=5.3.1'
    ]
)
