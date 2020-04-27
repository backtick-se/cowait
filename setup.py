import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cowait",
    version="0.1.0",
    author="Backtick Technologies",
    author_email="hello@backtick.se",
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
