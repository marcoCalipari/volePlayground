# Welcome to VOLE Playground!

This repository contains python implementations of:

 - 1-out-of-2 OT
 - 1-out-of-N OT
 - K-out-of-N OT
 - VOLE based on OT
 - VOLE based on Homomorphic encryption [Paillier]

Along with the actual code implementation, you will be able to find some basic examples on how to use the modules, as well as some basic benchmarking and profiling

# Disclamer 
This project is intended for demonstration purposes or for research projects focused on new functionalities developement.
It is not intended by all means to be a commercial solution that can guarantee security in the implementation!

# Repository structure
The repository is organized in 3 main folders:

 - **Modules**: The Modules folder contains the implementation of the modules. It's divided in two main foldes: **Functions**, where you can find the modules that you can implement in your code, and **Utils**, where you'll find some helpers functions and the necessary classes to start developing your VOLE project

 -  **Demo**: Contains simple examples on how to use each and every function


## How to get started with the repo

 1. Clone the repository
 `git clone https://github.com/jplaui/VOLE_testing.git`
 
 2. Change your branch: `git checkout VOLE_benchmarking`
 
 3. Activate the virtual environment in case you do not want to have conflicts: `source .venv/bin/activate`
	    
 4. install the required packages with `pip install -r requirements.txt`

 5. Start developing.

## How to run the demos

 1. Change you folder from the root to demos `cd Demos`
 2. From there you can directly run the scripts `python3 <name of the script>`

## How to develop custom projects using the provided modules:

0. Install the required packages in case you did not do that with `pip install -r requirements.txt`
1. Copy the Modules folder into your project folder
2. Start developing

# Known issues and future work
## Known issues:
 - [ ] Change the code structure so that we can use different type of inputs and not just integers
 - [ ] Publishing the module as a py module, so that we can directly install the OT module with pip
 ## Future work
 - [ ] Go translation

# Setup used:
- PC: MSI modern 15 i5
- Linux subsystem for windows [Debian distro]
- Python 3.9.2
- vscode for remote developing v. 1.77.1 x64
