from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="busypie",
    version="0.4.5",
    author="Eli Segal",
    author_email="eli.segal@gmail.com",
    license='Apache License 2.0',
    description="Easy and expressive busy-waiting for Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords="busy wait tdd test builder sleep wait pytest",
    url="https://github.com/rockem/busypie",
    packages=find_packages(exclude=['tests*']),
    setup_requires=["pytest-runner"],
    tests_require=[
        'pytest==5.4.3',
        'pytest-asyncio==0.12.0',
        'pytest-timeout==1.3.3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
