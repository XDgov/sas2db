import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sas2sqlite",
    version="0.1.0",
    author="Aidan Feldman",
    author_email="aidan.l.feldman@census.gov",
    description="Convert SAS files to SQLite databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XDgov/sas2sqlite",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'inflection',
        'pandas',
        'sqlalchemy',
    ],
    entry_points={
        'console_scripts': [
            'sas2sqlite = sas2sqlite.run:main'
        ]
    }
)
