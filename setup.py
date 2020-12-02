import setuptools

VERSION = '0.4.0'

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    name='cowait',
    version=VERSION,
    author='Backtick Technologies',
    description='Cowait is a framework for creating ' +
                'containerized workflows with asynchronous Python.',

    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/backtick-se/cowait',

    packages=['cowait'],
    entry_points={
        'console_scripts': [
            'cowait = cowait.__main__:main',
        ],
    },

    classifiers=[],

    python_requires='>=3.7',
    install_requires=requirements,
)
