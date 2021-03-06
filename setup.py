import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ScheTH",
    version="1.0.0",
    author="YJie",
    author_email="jieyaqi@msu.edu",
    description="A package for generating detailed study plan",
    url="https://github.com/Aaaapril4/Scheth",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)