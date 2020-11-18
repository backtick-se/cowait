import setuptools

VERSION = "0.3.5"

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

    packages=['cowait'],
    entry_points={
        'console_scripts': [
            'cowait = cowait.__main__:main',
        ],
    },

    classifiers=[],

    python_requires='>=3.6',

    install_requires=[
        'click',
        'docker',
        'requests < 2.25',
        'pyyaml',
        'dask',
        'distributed',
        'kubernetes < 12',
        'pyyaml',
        'marshmallow',
        'aiohttp',
        'aiohttp-middlewares',
        'pytest',
        'pytest-sugar',
        'pytest-cov',
        'alt-pytest-asyncio',
        'nest-asyncio',
        'numpy',
        'sty',
        'jupyterlab',
        'dill',
        'python-dotenv',
        'fsspec',
        's3fs',
    ],
)
