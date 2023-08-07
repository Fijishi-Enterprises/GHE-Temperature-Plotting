import numpy as np
import pandas as pd
from pytest import raises

from GHEtool import Borefield, GroundConstantTemperature, MonthlyGeothermalLoadAbsolute
from GHEtool.functions.size_borefield_config import NoBorefieldFoundError, size_borefield

def test_borefield_sizing_raise_error():
    # relevant borefield data for the calculations
    data = GroundConstantTemperature(3,             # conductivity of the soil (W/mK)
                                     10,            # Ground temperature at infinity (degrees C)
                                     2.4 * 10**6)   # ground volumetric heat capacity (J/m3K)

    # monthly loading values
    peak_cooling = np.array([0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.])  # Peak cooling in kW
    peak_heating = np.array([160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.])  # Peak heating in kW

    # annual heating and cooling load
    annual_heating_load = 300 * 10 ** 3  # kWh
    annual_cooling_load = 160 * 10 ** 3  # kWh

    # percentage of annual load per month (15.5% for January ...)
    monthly_load_heating_percentage = np.array([0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144])
    monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])

    # resulting load per month
    monthly_load_heating = annual_heating_load * monthly_load_heating_percentage   # kWh
    monthly_load_cooling = annual_cooling_load * monthly_load_cooling_percentage   # kWh

    # set the load
    load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)

    # create the borefield object
    borefield = Borefield(load=load)

    # one can activate or deactive the logger, by default it is deactivated
    # borefield.activate_logger()
    # borefield.deactivate_logger()

    borefield.set_ground_parameters(data)
    rect_field = borefield.create_rectangular_borefield(10, 12, 6, 6, 100, 4, 0.075)
    rect_field.max_length = 5
    rect_field.max_width = 5
    rect_field.depth_max = 95

    borefield.Rb = 0.12  # equivalent borehole resistance (K/W)

    # set temperature boundaries
    borefield.set_max_ground_temperature(16)   # maximum temperature
    borefield.set_min_ground_temperature(0)    # minimum temperature

    with raises(NoBorefieldFoundError):
        size_borefield(borefield)


def test_borefield_sizing_method_rectangular():
    # relevant borefield data for the calculations
    data = GroundConstantTemperature(3,             # conductivity of the soil (W/mK)
                                     10,            # Ground temperature at infinity (degrees C)
                                     2.4 * 10**6)   # ground volumetric heat capacity (J/m3K)

    # monthly loading values
    peak_cooling = np.array([0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.])  # Peak cooling in kW
    peak_heating = np.array([160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.])  # Peak heating in kW

    # annual heating and cooling load
    annual_heating_load = 300 * 10 ** 3  # kWh
    annual_cooling_load = 160 * 10 ** 3  # kWh

    # percentage of annual load per month (15.5% for January ...)
    monthly_load_heating_percentage = np.array([0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144])
    monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025])

    # resulting load per month
    monthly_load_heating = annual_heating_load * monthly_load_heating_percentage   # kWh
    monthly_load_cooling = annual_cooling_load * monthly_load_cooling_percentage   # kWh

    # set the load
    load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)

    # create the borefield object
    borefield = Borefield(load=load)

    # one can activate or deactive the logger, by default it is deactivated
    # borefield.activate_logger()
    # borefield.deactivate_logger()

    borefield.set_ground_parameters(data)
    rect_field = borefield.create_rectangular_borefield(10, 12, 6, 6, 100, 4, 0.075)
    rect_field.max_length = 30
    rect_field.max_width = 20
    rect_field.depth_max = 95

    borefield.Rb = 0.12  # equivalent borehole resistance (K/W)

    # set temperature boundaries
    borefield.set_max_ground_temperature(16)   # maximum temperature
    borefield.set_min_ground_temperature(0)    # minimum temperature

    configs = size_borefield(borefield)
    min_number = configs[0][1] * configs[0][2]

    """
    n_min_manual = (999,99,99)
    li = []
    for n_1 in range(2, rect_field.max_length + 2):
        for n_2 in range(2, rect_field.max_width + 2):
            #if n_min_manual[0] <= n_1 * n_2:
            #    continue
            borefield.create_rectangular_borefield(n_1, n_2, rect_field.max_length / (n_1 - 1), rect_field.max_width / (n_2 - 1), rect_field.depth_max, 4,
                                                   0.075)
            borefield.calculate_temperatures(rect_field.depth_max)
            li.append((n_1*n_2, np.max(borefield.results_peak_cooling) - borefield.Tf_max, np.min(borefield.results_peak_heating)- borefield.Tf_min))
            if np.max(borefield.results_peak_cooling) <= borefield.Tf_max and np.min(borefield.results_peak_heating)>= borefield.Tf_min:
                n_min_manual = (n_1 * n_2, n_1, n_2, rect_field.max_length / (n_1 - 1), rect_field.max_width / (n_2 - 1))
    pd.DataFrame(li).to_csv("test.csv")#"""
    assert min_number == 126


