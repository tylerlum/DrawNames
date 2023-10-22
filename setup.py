from setuptools import setup, find_packages
from pathlib import Path

VERSION = "0.0.1"
DESCRIPTION = "Customize-able Secret Santa Name List Generator"
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="DrawNames",
    version=VERSION,
    author="Tyler Lum",
    author_email="tylergwlum@gmail.com",
    url="https://github.com/tylerlum/DrawNames",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["typed-argparse"],
    keywords=["python", "secret santa", "draw names"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
