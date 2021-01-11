from setuptools import setup, find_packages

exec(open('cowait/version.py').read())

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='cowait',
    version=version,
    author='Backtick Technologies',
    description='Cowait is a framework for creating ' +
                'containerized workflows with asynchronous Python.',

    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/backtick-se/cowait',

    packages=find_packages(exclude=["test.*", "test"]),
    entry_points={
        'console_scripts': [
            'cowait = cowait.__main__:main',
        ],
    },

    classifiers=[],

    python_requires='>=3.7',
    install_requires=[
        'docker>=4',
        'kubernetes>=11,<13',
        'nest-asyncio>=1.4.1',
        'aiohttp>=3',
        'aiohttp-middlewares>=1',
        'pytest>=6',
        'alt-pytest-asyncio>=0.5.3',  # would be nice to move to the widely used pytest-asyncio
        'python-dotenv>=0.15',
        'fsspec',
        's3fs',
        'aiobotocore[boto3]',

        # cli
        'click>=7',
        'PyYAML>=5',
        'sty==1.0.0-beta.12',  # tty coloring, seems to be stuck in beta. remove/replace

        # convenient, but easy to get rid of
        'marshmallow >= 3',

        # utilities, not actually required
        'numpy >= 1',  # provides typing for numpy. unlikely to break
        'pytest-sugar >= 0.9',
        'pytest-cov >= 2',

        # extract to cowait-dask
        'dask >= 2',
        'distributed >= 2',
    ]
)
