import os

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

requirementsPath = '%s/requirements.txt' % os.path.dirname(os.path.realpath(__file__))
with open(requirementsPath) as f:
    requirements = [line for line in f.read().splitlines() if len(line) > 0],

setup(
    name="busypie",
    version="0.0.1",
    author="Eli Segal",
    author_email="eli.segal@gmail.com",
    description="Busy wait easy-peasy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rockem/busypie",
    packages=['busypie'],
    install_requires=[

    ],
    tests_requires=[
        'pytest==5.3.2',
        'pytest-runner==5.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache-2.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)