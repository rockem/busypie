import os

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="busypie",
    version="0.1.1",
    author="Eli Segal",
    author_email="eli.segal@gmail.com",
    license='Apache License 2.0',
    description="Busy wait easy-peasy",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/rockem/busypie",
    packages=['busypie'],
    setup_requires=["pytest-runner"],
    install_require=[

    ],
    tests_require=[
        'pytest==5.3.2',
        'pytest-timeout==1.3.3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)