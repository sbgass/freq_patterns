import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="freq_patterns",
    version="0.0.0",
    author="Stephen Gass",
    author_email="",
    description="Frequent Pattern Mining Algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sbgass/freq_patterns",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ),
)
