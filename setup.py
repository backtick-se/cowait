import setuptools

VERSION = "0.2.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cowait",
    version=VERSION,
    author="Backtick Technologies",
    description="Cowait is a framework for creating " +
                "containerized workflows with asynchronous Python.",

    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/backtick-se/cowait",

    packages=setuptools.find_packages(),
    scripts=['bin/cowait'],

    classifiers=[],

    python_requires='>=3.6',

    install_requires=[
        'click',
        'docker',
        'requests',
        'pyyaml',
        'dask',
        'distributed',
        'kubernetes',
        'pyyaml',
        'marshmallow',
        'aiohttp',
        'pytest',
        'pytest-sugar',
        'pytest-cov',
        'pytest-asyncio',
        'nest-asyncio',
    ],
)
