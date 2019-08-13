from os import path
from setuptools import setup


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="edx-backup",
    description="Backup and restore edx databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["edxbackup"],
    install_requires=["click", "python-swiftclient", "python-keystoneclient", "cryptography"],
    entry_points={"console_scripts": ["edxbackup=edxbackup.cli:main"]},
)
