import setuptools

with open("README.md", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyFAT",
    version="0.0.2",
    author="Kevan Gahan",
    author_email="gahank@oregonstate.edu",
    license='MIT',
    description="This package analyzes .csv files created by material test systems to determine monotonic or fatigue material properties",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SoftwareDevEngResearch/PyFAT",
    packages=setuptools.find_packages(),
    package_dir = {
        'pyfat':'pyfat',
        'pyfat.tests':'pyfat/tests'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        'pytest','matplotlib','numpy','pandas','pathlib','argparse',
        'datetime',
        ]
)