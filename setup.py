from setuptools import setup

setup(
    name="mayatdd",
    version="0.0.1",
    packages=["mayatdd"],
    include_package_data = True,
    install_requires=[
        "dccautomation"],

    dependency_links=[
        "git+ssh://git@github.com:rgalanakis/dccautomation.git#egg=dccautomation-0.1.0"
    ],
)
