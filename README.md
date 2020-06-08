# PyFAT Overview
Python FATigue Testing Data Analysis Package

This Software package contains comprehensive and intuitive automated analysis for 
polymer or composite material test data (both monotonic tensile and fatigue testing). 
The package will read and analyze numerous .csv files created by material test systems 
throughout a testing program for any plastic or composite material.

Historically, material test engineers would analyze .csv files one-by-one to retrieve
the necessary information (test parameters, material properties, etc.). This process
was time consuming and tedious. PyFAT fixes that problem, providing the ability to 
analyze numerous files quickly, determining all necessary parameters and creating
high quality, convenient plot of both monotontic and fatgiue characteristics.

**PyFAT contains two main analysis techniques: "monotonic" and "fatigue".**


# Monotonic Analysis
This functionality is used to analyze a directory containing only .csv files
created from monotonic tensile testing. This analysis outputs the following material
parameters in a .csv file:
* Starting position (mm), failure positon (mm), nominal extension (mm)
* Poisson's ratio
* Tensile Modulus (or "Elastic Modulus", if applicable) (GPa)
* 0.2% offset stress (MPa) and strain (m/m)
* Yield Stress (Mpa) and strain (m/m)
    Note: for plastics/composites, the yield point and 0.2% offset point may not be the same.
* Maximum Load (kN)
* Ultimate true Stress (MPa), Ultimte True Ductility (m/m)
* Max Axial Strain (%) and Max Transverse Strain (%)

**The monotonic analysis assumes the following:**
* The material being tested is a plastic or composite material.
* All testing parameters are equivalent between each test.
* A single, displacement-controlled deformation rate occurs throughout every test.
* The data contains either a channel for stress (MPa) or the sample width and thickness for stress to be calculated.

**The data .csv files must contain (at a minimum) the following columns (channels):**
* Position (mm) with "Position" in the column header name.
* Load (kN) with "Load" in the column header name.
* Axial Strain (%) with "Axial Strain" in the column header name.
* Transverse Strain (%) with "Transverse Strain" in the column header name.
 
**The data .csv file must also contain ONE of the following options:**
* Stress (MPa) with "Stress" in the header name.
OR
* Sample width and thickness (mm) in columns labeled "width" and "thickness", respectively.

The monotonic analysis functionality also saves a high-quality .tiff image of the stress-
strain curve for every test. It also outputs one stress-strain curve with all of the tests
overlaid onto one plot.

# Fatigue Analysis
This functionality is used to analyze a directory containing only .csv files
created from fatigue tensile testing at any test fequency. This analysis outputs 
the "Half-Life" parameters (for every test) in a .csv file:
* Cycles-to-Failure
* True Stress Range (Max - Min) (Pa)
* True Stress Amplitude (Pa)
* Total Strain Amplitude (m/m)
* Plastic Strain Amplitude (m/m)
* Elastic Strain Amplitude (m/m)

**The following material parameters will also be listed in a .log file:**
* Strain-Life Fatigue Parameters:
    * Fatigue Strength Coefficient (σf') (MPa)
    * Fatigue Strength Exponent (b)
    * Fatigue Ductility Coefficient (εf')
    * Fatigue Ductility Exponent (c)
* Stress-Life Fatigue Parameters:
    * Stress-Range Intercept (SRI1) (MPa)
    * Stress-Life Exponent (slope)
* Standard-Errors for Stress-Life, Elastic Strain-Life, Plastic Strain-Life

**The Fatigue analysis assumes the following:**
* The material being tested is a plastic or composite material.
* The fatigue test frequency varies between tests within the bounds of 1 Hz to 10 Hz.
* Fatigue testing is conducted in strain-control using an axial extensometer.
* The data contains either a channel for stress (MPa) or the sample width and thickness for stress to be calculated.

**The data .csv files must contain (at a minimum) the following columns (channels):**
* Cycle count 
* Maximum Load (kN) with "max" and "load" in the column header name.
* Minimum Load (kN) with "min" and "load" in the column header name.
* Maximum Axial Strain (%) with "max" and "Axial Strain" in the column header name.
* Minimum Axial Strain (%) with "min" and "Axial Strain" in the column header name.

**The data .csv file must also contain ONE of the following options:**
* Maximum Stress (MPa) with "max" and "stress" in the column header name.
* Minimum Stress (MPa) with "min" and "stress" in the column header name.
OR
* Sample width and thickness (mm) in columns labeled "width" and "thickness", respectively.

The Fatigue analysis also saves a high-quality .tiff image of the following plots:
* Stress-Range vs. Reversals-to-Failure (Stress-Life)
* Plastic Strain-Amplitude vs. Reversals-to-Failure (Plastic Strain-Life)
* Elastic Strain-Amplitude vs. Reversals-to-Failure (Elastic Strain-Life)
* Total Strain Amplitude vs. Cycles-to-Failure
* Plastic, Elastic, and Total Strain-Amplitude vs. Cycles-to-Failure (Total Strain-Life)

# User Inputs
PyFAT takes in several user inputs, one of which is an input file that tells the program 
where the test data files are located as well as where to output the results...

**To format the input file correctly:**
* Use a .txt file format
* Use the character "#" at the beginning of a line for comments.
    * Lines starting with # will be ignored by the program.
* Write a line with "INPUT = " or "INPUT=" (Spaces dont matter) followed by the path to where the test data .csv files are located.
    * Example: INPUT = /path/to/input/files
* Write a line with "OUTPUT = " or "OUTPUT=" (Spaces dont matter) followed by the path to where the user wants the results to be saved.
    * Example: OUTPUT = /path/to/output/location

**Other User Inputs (Argparse inputs):**

-m: Run monotonic analysis 
-f: Run Fatigue analysis
-e: Elastic Modulus. The -e option is given ONLY when -f is chosen for fatigue.
    **The -e option must be followed by the material's elastic modulus in MPa**
    Example: -e 1902 (if the material's elastic modulud is 1902 MPa)

# Summary of Provided Examples
Two examples are provided with PyFAT, one for Monotonic analysis and another for Fatigue analysis.

The example content is located in the "example" folder: **PyFAT/example**

The example folder contains the following items:
* A Folder called "Monotonic" containing the provided example monotonic data .csv files.
* A Folder called "Fatigue" containing the provided example fatigue data .csv files.
* monotonic_input.txt - the example monotonic input file that is formatted correctly but will need to be updated with correct file paths.
* fatigue_input.txt - the example fatigue input file that is formatted correctly but will need to be updated with correct file paths.

# How to Run Provided Examples

**To Run the Monotonic Example:**
1. Edit the "monotonic_input.txt example input file"
    * Locate the file at PyFAT/example/monotonic_input.txt
    * Update the file with the following:
        * INPUT = {path to PyFAT on your computer}/PyFAT/example/monotonic
        * OUTPUT = {path to PyFAT on your computer}/PyFAT/example/output
2. Change into the pyfat directory: PyFAT/pyfat
3. Run the program with the following command:

    **python PyFAT.py {path to PyFAT on your computer}/PyFAT/example/monotonic_input.txt -m**

Note: The path to the input file is passed in first, followed by the -m command for monotonic analysis.

4. Wait for results.


**To Run the Fatigue Example:**
1. Edit the "fatigue_input.txt example input file"
    * Locate the file at PyFAT/example/fatigue_input.txt
    * Update the file with the following:
        * INPUT = {path to PyFAT on your computer}/PyFAT/example/fatigue
        * OUTPUT = {path to PyFAT on your computer}/PyFAT/example/output
2. Change into the pyfat directory: PyFAT/pyfat
3. Run the program with the following command:
    **python PyFAT.py {path to PyFAT on your computer}/PyFAT/example/fatigue_input.txt -f -e 1902**

Note: The path to the input file is passed in first, followed by the -f command for fatigue analysis,
      followed by the -e command for the elastic modulus followed by 1902 specifying an elastic modulus
      of 1902 MPa for the example material.

4. Wait for results.









