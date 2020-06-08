# PyFAT
Python FATigue Testing Data Analysis Package

This Software package contains comprehensive and intuitive automated analysis for 
polymer or composite material test data (both monotonic tensile and fatigue testing). 
The package will read and analyze numerous .csv files created by material test systems 
throughout a testing program for any plastic or composite material.

Historically, material test engineers would analyze .csv files one-by-one to retrieve
the necessary information (test parameters, material properties, etc.). This process
was time consuming and tedious. PyFAT fixes that problem, providing the ability to 
analyzed numerous files quickly, determining all necessary parameters and creating
high quality, convenient plot of both monotontic and fatgiue characteristics.

# Functionality 
PyFAT contains two main analysis techniques: "monotonic" and "fatigue".

The monotonic analysis assumes the following:
* The material being tested is a plastic or composite material.
* A single, displacement-controlled deformation rate occurs throughout every test
* The data contains either a channel for stress (MPa) or the sample width and thickness for stress to be calculated
* TEST


