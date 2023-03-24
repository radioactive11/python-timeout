from setuptools import setup, find_packages

VERSION = "1.0.0"
DESCRIPTION = "Timeout & retry functions in Python with a single line of code"
with open("README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="python-timeout",
    version=VERSION,
    packages=find_packages("python-timeout", exclude=("tests",)),
    install_requires=open("requirements.txt").readlines(),
    author="radioactive11",
    author_email="roy.arijit@icloud.com",
    url="https://github.com/radioactive11/python-timeout",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="python timeout retry kill signal unix",
)
