# GHEtool: An open-source tool for borefield sizing

[![PyPI version](https://badge.fury.io/py/GHEtool.svg)](https://badge.fury.io/py/GHEtool)
[![Tests](https://github.com/wouterpeere/GHEtool/actions/workflows/test.yml/badge.svg)](https://github.com/wouterpeere/GHEtool/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/wouterpeere/GHEtool/branch/main/graph/badge.svg?token=I9WWHW60OD)](https://codecov.io/gh/wouterpeere/GHEtool)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.04406/status.svg)](https://doi.org/10.21105/joss.04406)
[![Downloads](https://static.pepy.tech/personalized-badge/ghetool?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/ghetool)
[![Downloads](https://static.pepy.tech/personalized-badge/ghetool?period=week&units=international_system&left_color=black&right_color=orange&left_text=Downloads%20last%20week)](https://pepy.tech/project/ghetool)
[![Read the Docs](https://readthedocs.org/projects/ghetool/badge/?version=latest)](https://ghetool.readthedocs.io/en/latest/)
## What is *GHEtool*?

GHEtool is a Python package that contains all the functionalities needed to deal with borefield design. GHEtool has been developed as a joint effort of KU Leuven (The SySi Team), boydens engineering (part of Sweco) and FH Aachen.
The core of this package is the automated sizing of borefield under different conditions. By making use of combination of just-in-time calculations of thermal ground responses (using [pygfunction](https://github.com/MassimoCimmino/pygfunction)) with
intelligent interpolation, this automated sizing can be done in the order of milliseconds. Please visit our website [https://GHEtool.eu](https://GHEtool.eu) for more information.

#### Read The Docs
GHEtool has an elaborate documentation were all the functionalities of the tool are explained, with examples, literature and validation.
This can be found on [https://docs.ghetool.eu](https://docs.ghetool.eu).

#### Graphical user interface
GHEtool comes with a *graphical user interface (GUI)*. This GUI is built using [ScenarioGUI](https://github.com/tblanke/ScenarioGUI).
One can download the open-source GUI [here](https://ghetool.eu/wp-content/uploads/setups/GHEtool%20Community_setup_v2_2_0.exe).
<p align="center">
<img src="https://raw.githubusercontent.com/wouterpeere/GHEtool/main/docs/sources/gui/_figure/GHEtool.PNG" width="600">
</p>

### Development
GHEtool is in constant development with new methods, enhancements and features added to every new version. Please visit our [project board](https://github.com/users/wouterpeere/projects/2) to check our progress.

## Requirements
This code is tested with Python 3.8, 3.9, 3.10 and 3.11 and requires the following libraries (the versions mentioned are the ones with which the code is tested)

* Numpy (>=1.20.2)
* Scipy (>=1.6.2)
* Matplotlib (>=3.4.1)
* Pygfunction (>=2.2.2)
* Openpyxl (>=3.0.7)
* Pandas (>=1.2.4)

For the GUI

* ScenarioGUI (>=0.3.0)

For the tests

* Pytest (>=7.1.2)

## Quick start
### Installation

One can install GHEtool by running Pip and running the command

```
pip install GHEtool
```

or one can install a newer development version using

```
pip install --extra-index-url https://test.pypi.org/simple/ GHEtool
```

Developers can clone this repository.

It is a good practise to use virtual environments (venv) when working on a (new) Python project so different Python and package versions don't conflict with eachother. For GHEtool, Python 3.8 or higher is recommended. General information about Python virtual environments can be found [here](https://docs.Python.org/3.9/library/venv.html) and in [this article](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).

### Check installation

To check whether everything is installed correctly, run the following command

```
pytest --pyargs GHEtool
```

This runs some predefined cases to see whether all the internal dependencies work correctly. All test should pass successfully.

## Get started with GHEtool

### Building blocks of GHEtool
GHEtool is a flexible package that can be extend with methods from [pygfunction](https://pygfunction.readthedocs.io/en/stable/) (and [ScenarioGUI](https://github.com/tblanke/ScenarioGUI) for the GUI part).
To work efficiently with GHEtool, it is important to understand the main structure of the package.

#### Borefield
The Borefield object is the central object within GHEtool. It is within this object that all the calculations and optimizations take place.
All attributes (ground properties, load data ...) are set inside the borefield object.

#### Ground properties
Within GHEtool, there are multiple ways of setting the ground data. Currently, your options are:

* _GroundConstantTemperature_: if you want to model your borefield with a constant, know ground temperature.
* _GroundFluxTemperature_: if you want to model your ground with a varying ground temperature due to a constant geothermal heat flux.
* _GroundTemperatureGradient_: if you want to model your ground with a varying ground temperature due to a geothermal gradient.

Please note that it is possible to add your own ground types by inheriting the attributes from the abstract _GroundData class.

#### Pipe data
Within GHEtool, you can use different structures for the borehole internals: U-tubes or coaxial pipes.
Concretely, the classes you can use are:

* _Multiple U-tubes_
* _Single U-tubes (special case of multiple U-tubes)_
* _Double U-tubes (special case of multiple U-tubes)_
* _Coaxial pipe_
 
Please note that it is possible to add your own pipe types by inheriting the attributes from the abstract _PipeData class.

#### Fluid data
You can set the fluid data by using the FluidData class. In the future, more fluid data classes will be made available.

#### Load data
One last element which you will need in your calculations, is the load data. Currently, you can only set the primary (i.e. geothermal) load of the borefield.
In a future version of GHEtool, also secundary building loads will be included. For now, you can use the following inputs:

* _MonthlyGeothermalLoadAbsolute_: You can set one the monthly baseload and peak load for heating and cooling for one standard year which will be used for all years within the simulation period.
* _HourlyGeothermalLoad_: You can set (or load) the hourly heating and cooling load of a standard year which will be used for all years within the simulation period.
* _HourlyGeothermalLoadMultiYear_: You can set (or load) the hourly heating and cooling load for multiple years (i.e. for the whole simulation period). This way, you can use secundary loads already with GHEtool as shown in [this example](https://ghetool.readthedocs.io/en/stable/sources/code/Examples/active_passive_cooling.html).

All load classes also have the option to add a yearly domestic hot water usage.

Please note that it is possible to add your own load types by inheriting the attributes from the abstract _LoadData class.

### Options for sizing methods
Like always with iterative methods, there is a trade-off between speed and accuracy. Within GHEtool (using the CalculationSetup class) one can alter different parameters
to customize the behaviour they want. Note that these options are additive, meaning that, for example, the strongest criteria from the
atol and rtol is chosen when sizing. The options are:

* _atol_: For the sizing methods, an absolute tolerance in meters between two consecutive iterations can be set.
* _rtol_: For the sizing methods, a relative tolerance in meters between two consecutive iterations can be set.
* _max_nb_of_iterations_: For the sizing methods, a maximum number of iterations can be set. If the size is not converged, a RuntimeError is thrown.
* _use_precalculated_dataset_: This option makes sure the custom g-function dataset (if available) is not used.
* _interpolate_gfunctions_: Calculating the gvalues gives a large overhead cost, although they are not that sensitive to a change in borehole depth. If this parameter is True 
it is allowed that gfunctions are interpolated. (To change the threshold for this interpolation, go to the Gfunction class.)
* _deep_sizing_: An alternative sizing method for cases with high cooling (peaks) and a variable ground temperature.
This method is potentially slower, but proves to be more robust.
* _force_deep_sizing_: When the alternative method from above should always be used.

### Simple example

To show how all the pieces of GHEtool work together, below you can find a step-by-step example of how, traditionally, one would work with GHEtool.
Start by importing all the relevant classes. In this case we are going to work with a ground model which assumes a constant ground temperature (e.g. from a TRT-test),
and we will provide the load with a monthly resolution.

```Python
from GHEtool import Borefield, GroundDataConstantTemperature, MonthlyGeothermalLoadAbsolute
```

After importing the necessary classes, the relevant ground data parameters are set.

```Python
data = GroundDataConstantTemperature(3,   # ground thermal conductivity (W/mK)
                                     10,  # initial/undisturbed ground temperature (deg C)
                                     2.4*10**6) # volumetric heat capacity of the ground (J/m3K) 
```

Furthermore, for our loads, we need to set the peak loads as well as the monthly base loads for heating and cooling.

```Python
peak_cooling = [0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.]   # Peak cooling in kW
peak_heating = [160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.]  # Peak heating in kW

monthly_load_heating = [46500.0, 44400.0, 37500.0, 29700.0, 19200.0, 0.0, 0.0, 0.0, 18300.0, 26100.0, 35100.0, 43200.0]        # in kWh
monthly_load_cooling = [4000.0, 8000.0, 8000.0, 8000.0, 12000.0, 16000.0, 32000.0, 32000.0, 16000.0, 12000.0, 8000.0, 4000.0]  # in kWh

# set load object
load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)

```

Next, we create the borefield object in GHEtool and set the temperature constraints and the ground data.
Here, since we do not use a pipe and fluid model (see [Examples](https://ghetool.readthedocs.io/en/stable/sources/code/examples.html) if you need examples were no borehole thermal resistance is given),
we set the borehole equivalent thermal resistance.

```Python
# create the borefield object
borefield = Borefield(load=load)

# set ground parameters
borefield.set_ground_parameters(data)

# set the borehole equivalent resistance
borefield.Rb = 0.12

# set temperature boundaries
borefield.set_max_avg_fluid_temperature(16)  # maximum temperature
borefield.set_min_avg_fluid_temperature(0)  # minimum temperature
```

Next we create a rectangular borefield.

```Python
# set a rectangular borefield
borefield.create_rectangular_borefield(10, 12, 6, 6, 110, 4, 0.075)
```

Note that the borefield can also be set using the [pygfunction](https://pygfunction.readthedocs.io/en/stable/) package, if you want more complex designs.

```Python
import pygfunction as gt

# set a rectangular borefield
borefield_gt = gt.boreholes.rectangle_field(10, 12, 6, 6, 110, 1, 0.075) 
borefield.set_borefield(borefield_gt)
```

Once a Borefield object is created, one can make use of all the functionalities of GHEtool. One can for example size the borefield using:

```Python
depth = borefield.size()
print("The borehole depth is: ", depth, "m")
```

Or one can plot the temperature profile by using

```Python
borefield.print_temperature_profile(legend=True)
```

A full list of functionalities is given below.

## Functionalities
GHEtool offers functionalities of value to all different disciplines working with borefields. The features are available both in the code environment and in the GUI.
For more information about the functionalities of GHEtool, please visit the documentation on [https://docs.ghetool.eu](https://docs.ghetool.eu).

