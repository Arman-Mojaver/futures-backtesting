from setuptools import find_packages, setup

setup(
    name="bt-cli",
    version="0.1",
    packages=find_packages(),
    install_requires=["click"],
    entry_points={"console_scripts": ["bt=cli.main:main"]},
)
