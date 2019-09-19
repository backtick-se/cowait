import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pipeline",
    version="0.0.4",
    author="castle",
    author_email="author@example.com",
    description="castle pipeline client",

    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/castle/data-science-pipeline",

    packages=setuptools.find_packages(),
    scripts=['bin/pipeline'],

    classifiers=[ ],

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
    'pyzmq',
],
"""