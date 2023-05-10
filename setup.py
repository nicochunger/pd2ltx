import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pd2ltx",
    author="Nicolas Unger",
    author_email="nicolas.unger@unige.ch",
    version="0.1.0",
    description="Conversion from pandas DataFrame to LaTeX table with support for error bars.",
    long_description=long_description,
    long_description_text_type="text/markdown",
    url="https://github.com/nicochunger/pd2ltx",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "pandas"],
    classifiers=["Programming Language :: Python :: 3"],
)
