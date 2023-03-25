from setuptools import setup, find_packages

import os

here = os.path.abspath(os.path.dirname(__file__))

# Getting long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


VERSION = "1.0.5"
DESCRIPTION = "Timeout & retry functions in Python with a single line of code"

# Setting up
setup(
    name="pyrtout",
    version=VERSION,
    author="Arijit Roy (radioactive11)",
    author_email="<roy.arijit@icloud.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
)
