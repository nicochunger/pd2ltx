from setuptools import find_packages, setup

setup(
    name="pd2ltx",
    author="Nicolas Unger",
    author_email="nicolas.unger@unige.ch",
    description="Function to convert a pandas DataFrame to a LaTex table with support for error bars.",
    url="https://github.com/nicochunger/pd2ltx",
    packages=find_packages(),
    # package_dir={"": "src"},
)
