import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sas2db",
    version="0.2.1",
    author="Aidan Feldman",
    author_email="aidan.l.feldman@census.gov",
    description="Import SAS files to SQL databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XDgov/sas2db",
    packages=setuptools.find_packages(),
    python_requires='>=3',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'inflection>0.3,<1',
        'pandas>0.24,<1',
        'sqlalchemy>1.3,<2',
    ],
    entry_points={
        'console_scripts': [
            'sas2db = sas2db.run:main'
        ]
    }
)
