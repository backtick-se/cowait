import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cowait",
    version="0.0.5",
    author="Backtick Technologies AB",
    author_email="johan@backtick.se",
    description="Cowait Core",

    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/backtick-se/cowait",

    packages=setuptools.find_packages(),
    scripts=['bin/cowait'],

    classifiers=[],

    python_requires='>=3.6',
)

"""
install_requires=[
    'click',
    'docker',
    'requests',
    'pyyaml',
    'dask',
    'distributed',
    'kubernetes',
],
"""
