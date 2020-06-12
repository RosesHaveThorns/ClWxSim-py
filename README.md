# Climate Weather Sim
A very simplistic weather simulator.

## Current Features
- Wind Simulation
- Pressure Advection and Diffusion

## Future Features
- Coriolis Effect
- Temperature Calculation, using ideal gas laws and the Pressure Simulation
- Humidity Simulation, including Precipitation and Cloud tracking
- UI with front tracking and views for humidity, temperatures, pressure, wind etc
- Ability to input any Planet map into the simulation
- Simulation state storage and continuation

## Installation
- 1: download this repo as a zip from above
- 2: extract the repo and run "python setup.py install"
- 3: locate the package in the python directory and run "ClWxSim/ui/ClWxSim_Main.py" to run the simulator

### Possible Installation Issues
#### "error: Microsoft Visual C++ 14.0 is required"
Download the Visual Studio C++ build tools from https://visualstudio.microsoft.com/visual-cpp-build-tools/
#### "RuntimeError: Running cythonize failed!"
Install Cython prior to install using "pip install cython"
