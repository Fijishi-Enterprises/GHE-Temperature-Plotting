import math

import numpy as np
import pandas as pd
from pytest import raises

from GHEtool import Borefield, GroundConstantTemperature, MonthlyGeothermalLoadAbsolute
from GHEtool.functions.size_borefield_config import NoBorefieldFoundError, size_borefield


def test_borefield_sizing_raise_error():
    # relevant borefield data for the calculations
    data = GroundConstantTemperature(3,  # conductivity of the soil (W/mK)
                                     10,  # Ground temperature at infinity (degrees C)
                                     2.4 * 10 ** 6)  # ground volumetric heat capacity (J/m3K)

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
    monthly_load_heating = annual_heating_load * monthly_load_heating_percentage  # kWh
    monthly_load_cooling = annual_cooling_load * monthly_load_cooling_percentage  # kWh

    # set the load
    load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)

    # create the borefield object
    borefield = Borefield(load=load)

    # one can activate or deactive the logger, by default it is deactivated
    # borefield.activate_logger()
    # borefield.deactivate_logger()

    borefield.set_ground_parameters(data)
    rect_field = borefield.create_rectangular_borefield(10, 12, 6, 6, 100, 4, 0.075)
    rect_field.max_length_x = 5
    rect_field.max_length_y = 5
    rect_field.depth_max = 95

    borefield.Rb = 0.12  # equivalent borehole resistance (K/W)

    # set temperature boundaries
    borefield.set_max_ground_temperature(16)  # maximum temperature
    borefield.set_min_ground_temperature(0)  # minimum temperature

    with raises(NoBorefieldFoundError):
        size_borefield(borefield)


def test_borefield_sizing_method_rectangular():
    # relevant borefield data for the calculations
    data = GroundConstantTemperature(3,  # conductivity of the soil (W/mK)
                                     10,  # Ground temperature at infinity (degrees C)
                                     2.4 * 10 ** 6)  # ground volumetric heat capacity (J/m3K)

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
    monthly_load_heating = annual_heating_load * monthly_load_heating_percentage  # kWh
    monthly_load_cooling = annual_cooling_load * monthly_load_cooling_percentage  # kWh

    # set the load
    load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)

    # create the borefield object
    borefield = Borefield(load=load)

    # one can activate or deactivate the logger, by default it is deactivated
    # borefield.activate_logger()
    # borefield.deactivate_logger()

    borefield.set_ground_parameters(data)
    rect_field = borefield.create_rectangular_borefield(10, 12, 6, 6, 100, 4, 0.075)
    rect_field.max_length_x = 30.1
    rect_field.max_length_y = 20.4
    rect_field.depth_max = 95
    rect_field.min_distance = 2
    n_max = int(rect_field.max_length_x / rect_field.min_distance + 1) * int(rect_field.max_length_y / rect_field.min_distance + 1)
    max_config = rect_field.update_config(n_max)
    assert max_config[0][1] == int(rect_field.max_length_x / rect_field.min_distance + 1)
    assert max_config[0][2] == int(rect_field.max_length_y / rect_field.min_distance + 1)
    assert len(rect_field.li_boreholes) == n_max

    borefield.Rb = 0.12  # equivalent borehole resistance (K/W)

    # set temperature boundaries
    borefield.set_max_ground_temperature(16)  # maximum temperature
    borefield.set_min_ground_temperature(0)  # minimum temperature

    configs = size_borefield(borefield)
    assert borefield.number_of_boreholes == configs[0][1] * configs[0][2]
    min_number = borefield.number_of_boreholes

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
    for config in configs:
        assert config[3] >= rect_field.min_distance
        assert config[4] >= rect_field.min_distance

        assert np.isclose((config[1] - 1) * config[3], rect_field.max_length_x)
        assert np.isclose((config[2] - 1) * config[4], rect_field.max_length_y)

    configs = size_borefield(borefield, check_configs=True)
    assert borefield.number_of_boreholes == configs[0][1] * configs[0][2]
    min_number = borefield.number_of_boreholes
    assert min_number == 126


def test_borefield_sizing_method_box():
    # relevant borefield data for the calculations
    data = GroundConstantTemperature(3,  # conductivity of the soil (W/mK)
                                     10,  # Ground temperature at infinity (degrees C)
                                     2.4 * 10 ** 6)  # ground volumetric heat capacity (J/m3K)

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
    monthly_load_heating = annual_heating_load * monthly_load_heating_percentage  # kWh
    monthly_load_cooling = annual_cooling_load * monthly_load_cooling_percentage  # kWh

    # set the load
    load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)

    # create the borefield object
    borefield = Borefield(load=load)

    # one can activate or deactive the logger, by default it is deactivated
    # borefield.activate_logger()
    # borefield.deactivate_logger()

    borefield.set_ground_parameters(data)
    box_field = borefield.create_box_borefield(10, 12, 6, 6, 100, 4, 0.075)
    box_field.max_length_x = 50
    box_field.max_length_y = 40
    box_field.depth_max = 95
    box_field.min_distance = 2.0
    n_max = 2 * int(box_field.max_length_x / box_field.min_distance + 1) + 2 * int(box_field.max_length_y / box_field.min_distance + 1) - 4
    max_config = box_field.update_config(n_max)
    assert max_config[0][1] == int(box_field.max_length_x / box_field.min_distance + 1)
    assert max_config[0][2] == int(box_field.max_length_y / box_field.min_distance + 1)
    assert len(box_field.li_boreholes) == n_max

    borefield.Rb = 0.12  # equivalent borehole resistance (K/W)

    # set temperature boundaries
    borefield.set_max_ground_temperature(16)  # maximum temperature
    borefield.set_min_ground_temperature(0)  # minimum temperature

    configs = size_borefield(borefield)
    assert borefield.number_of_boreholes == configs[0][1] * 2 + 2 * (configs[0][2] - 2)
    min_number = borefield.number_of_boreholes
    """
    n_min_manual = (999,99,99)
    li = []
    for n_1 in range(2, rect_field.max_length + 2):
        for n_2 in range(2, rect_field.max_width + 2):
            if n_min_manual[0] <= 2*n_1 +2* (n_2-2):
                continue
            borefield.create_box_borefield(n_1, n_2, rect_field.max_length / (n_1 - 1), rect_field.max_width / (n_2 - 1), rect_field.depth_max, 4,
                                                   0.075)
            borefield.calculate_temperatures(rect_field.depth_max)
            li.append((2*n_1 +2* (n_2-2), np.max(borefield.results_peak_cooling) - borefield.Tf_max, np.min(borefield.results_peak_heating)- borefield.Tf_min))
            if np.max(borefield.results_peak_cooling) <= borefield.Tf_max and np.min(borefield.results_peak_heating)>= borefield.Tf_min:
                n_min_manual = (2*n_1 +2* (n_2-2), n_1, n_2, rect_field.max_length / (n_1 - 1), rect_field.max_width / (n_2 - 1))
    pd.DataFrame(li).to_csv("test.csv")
    print(n_min_manual)#"""
    assert min_number == 88
    for config in configs:
        assert config[3] >= box_field.min_distance
        assert config[4] >= box_field.min_distance

        assert np.isclose((config[1] - 1) * config[3], box_field.max_length_x)
        assert np.isclose((config[2] - 1) * config[4], box_field.max_length_y)

    configs = size_borefield(borefield, check_configs=True)
    assert borefield.number_of_boreholes == configs[0][1] * 2 + 2 * (configs[0][2] - 2)
    min_number = borefield.number_of_boreholes
    assert min_number == 88


def test_borefield_sizing_method_l():
    # relevant borefield data for the calculations
    data = GroundConstantTemperature(3,  # conductivity of the soil (W/mK)
                                     10,  # Ground temperature at infinity (degrees C)
                                     2.4 * 10 ** 6)  # ground volumetric heat capacity (J/m3K)

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
    monthly_load_heating = annual_heating_load * monthly_load_heating_percentage  # kWh
    monthly_load_cooling = annual_cooling_load * monthly_load_cooling_percentage  # kWh

    # set the load
    load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)

    # create the borefield object
    borefield = Borefield(load=load)

    # one can activate or deactive the logger, by default it is deactivated
    # borefield.activate_logger()
    # borefield.deactivate_logger()

    borefield.set_ground_parameters(data)
    l_field = borefield.create_L_shaped_borefield(10, 12, 6, 6, 100, 4, 0.075)
    l_field.max_length_x = 50
    l_field.max_length_y = 60
    l_field.depth_max = 150
    l_field.min_distance = 2.0
    n_max = int(l_field.max_length_x / l_field.min_distance + 1) + int(l_field.max_length_y / l_field.min_distance + 1) - 1
    max_config = l_field.update_config(n_max)
    assert max_config[0][1] == int(l_field.max_length_x / l_field.min_distance + 1)
    assert max_config[0][2] == int(l_field.max_length_y / l_field.min_distance + 1)
    assert len(l_field.li_boreholes) == n_max

    borefield.Rb = 0.12  # equivalent borehole resistance (K/W)

    # set temperature boundaries
    borefield.set_max_ground_temperature(16)  # maximum temperature
    borefield.set_min_ground_temperature(0)  # minimum temperature

    configs = size_borefield(borefield)
    assert borefield.number_of_boreholes == configs[0][1] + configs[0][2] - 1
    """
    n_min_manual = (999,99,99)
    li = []
    for n_1 in range(2, rect_field.max_length + 2):
        for n_2 in range(2, rect_field.max_width + 2):
            if n_min_manual[0] <= n_1 +(n_2-1):
                continue
            borefield.create_L_shaped_borefield(n_1, n_2, rect_field.max_length / (n_1 - 1), rect_field.max_width / (n_2 - 1), rect_field.depth_max, 4,
                                                   0.075)
            borefield.calculate_temperatures(rect_field.depth_max)
            li.append((n_1 +(n_2-1), np.max(borefield.results_peak_cooling) - borefield.Tf_max, np.min(borefield.results_peak_heating)- borefield.Tf_min))
            if np.max(borefield.results_peak_cooling) <= borefield.Tf_max and np.min(borefield.results_peak_heating)>= borefield.Tf_min:
                n_min_manual = (n_1 +(n_2-1), n_1, n_2, rect_field.max_length / (n_1 - 1), rect_field.max_width / (n_2 - 1))
    pd.DataFrame(li).to_csv("test.csv")
    print(n_min_manual)#"""
    assert borefield.number_of_boreholes == 56
    for config in configs:
        assert config[3] >= l_field.min_distance
        assert config[4] >= l_field.min_distance

        assert np.isclose((config[1] - 1) * config[3], l_field.max_length_x)
        assert np.isclose((config[2] - 1) * config[4], l_field.max_length_y)

    configs = size_borefield(borefield, check_configs=True)
    assert borefield.number_of_boreholes == configs[0][1] + configs[0][2] - 1
    assert borefield.number_of_boreholes == 56


def test_borefield_sizing_method_u():
    # relevant borefield data for the calculations
    data = GroundConstantTemperature(3,  # conductivity of the soil (W/mK)
                                     10,  # Ground temperature at infinity (degrees C)
                                     2.4 * 10 ** 6)  # ground volumetric heat capacity (J/m3K)

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
    monthly_load_heating = annual_heating_load * monthly_load_heating_percentage  # kWh
    monthly_load_cooling = annual_cooling_load * monthly_load_cooling_percentage  # kWh

    # set the load
    load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)

    # create the borefield object
    borefield = Borefield(load=load)

    # one can activate or deactive the logger, by default it is deactivated
    # borefield.activate_logger()
    # borefield.deactivate_logger()

    borefield.set_ground_parameters(data)
    u_field = borefield.create_U_shaped_borefield(10, 12, 6, 6, 100, 4, 0.075)
    u_field.max_length = 50
    u_field.max_width = 60
    u_field.depth_max = 150
    u_field.min_distance = 5.
    n_max = int(u_field.max_length_x / u_field.min_distance + 1) + 2*int(u_field.max_length_y / u_field.min_distance + 1) - 2
    max_config = u_field.update_config(n_max)
    assert max_config[0][1] == int(u_field.max_length_x / u_field.min_distance + 1)
    assert max_config[0][2] == int(u_field.max_length_y / u_field.min_distance + 1)
    assert len(u_field.li_boreholes) == n_max

    borefield.Rb = 0.12  # equivalent borehole resistance (K/W)

    # set temperature boundaries
    borefield.set_max_ground_temperature(16)  # maximum temperature
    borefield.set_min_ground_temperature(0)  # minimum temperature

    configs = size_borefield(borefield)
    assert borefield.number_of_boreholes == configs[0][1] - 2 + 2 * configs[0][2]
    min_number = borefield.number_of_boreholes
    """
    n_min_manual = (999, 99, 99)
    li = []
    for n_1 in range(2, rect_field.max_length + 2):
        for n_2 in range(2, rect_field.max_width + 2):
            if n_min_manual[0] <= n_1 - 2 + 2 * n_2:
                continue
            borefield.create_U_shaped_borefield(n_1, n_2, rect_field.max_length / (n_1 - 1), rect_field.max_width / (n_2 - 1), rect_field.depth_max, 4,
                                                0.075)
            borefield.calculate_temperatures(rect_field.depth_max)
            li.append((n_1 - 2 + 2 * n_2, np.max(borefield.results_peak_cooling) - borefield.Tf_max, np.min(borefield.results_peak_heating) - borefield.Tf_min))
            if np.max(borefield.results_peak_cooling) <= borefield.Tf_max and np.min(borefield.results_peak_heating) >= borefield.Tf_min:
                n_min_manual = (n_1 - 2 + 2 * n_2, n_1, n_2, rect_field.max_length / (n_1 - 1), rect_field.max_width / (n_2 - 1))
    pd.DataFrame(li).to_csv("test.csv")
    print(n_min_manual)  # """
    assert min_number == 55
    for config in configs:
        assert config[3] >= u_field.min_distance
        assert config[4] >= u_field.min_distance

        assert np.isclose((config[1] - 1) * config[3], u_field.max_length_x)
        assert np.isclose((config[2] - 1) * config[4], u_field.max_length_y)

    configs = size_borefield(borefield, check_configs=True)
    assert borefield.number_of_boreholes == configs[0][1] - 2 + 2 * configs[0][2]
    min_number = borefield.number_of_boreholes
    assert min_number == 55


def test_borefield_sizing_method_circle():
    # relevant borefield data for the calculations
    data = GroundConstantTemperature(3,  # conductivity of the soil (W/mK)
                                     10,  # Ground temperature at infinity (degrees C)
                                     2.4 * 10 ** 6)  # ground volumetric heat capacity (J/m3K)

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
    monthly_load_heating = annual_heating_load * monthly_load_heating_percentage  # kWh
    monthly_load_cooling = annual_cooling_load * monthly_load_cooling_percentage  # kWh

    # set the load
    load = MonthlyGeothermalLoadAbsolute(monthly_load_heating, monthly_load_cooling, peak_heating, peak_cooling)

    # create the borefield object
    borefield = Borefield(load=load)

    # one can activate or deactive the logger, by default it is deactivated
    # borefield.activate_logger()
    # borefield.deactivate_logger()

    borefield.set_ground_parameters(data)
    circle_field = borefield.create_circular_borefield(10, 12, 100, 4, 0.075)
    circle_field.max_radius_center_2_boreholes = 50
    circle_field.depth_max = 150

    n_max = int(4*math.pi * circle_field.max_radius_center_2_boreholes / circle_field.min_distance)
    max_config = circle_field.update_config(n_max)
    assert max_config[0][1] == n_max
    assert len(circle_field.li_boreholes) == n_max

    borefield.Rb = 0.12  # equivalent borehole resistance (K/W)

    # set temperature boundaries
    borefield.set_max_ground_temperature(16)  # maximum temperature
    borefield.set_min_ground_temperature(0)  # minimum temperature

    configs = size_borefield(borefield)
    assert borefield.number_of_boreholes == configs[0][1]
    min_number = borefield.number_of_boreholes
    """
    n_min_manual = 9999
    li = []
    for n_1 in range(2, int(4*math.pi*circle_field.max_radius_center_2_boreholes / circle_field.min_distance)):
        if n_1 > n_min_manual:
            continue
        borefield.create_circular_borefield(n_1, circle_field.max_radius_center_2_boreholes, circle_field.depth_max, 4, 0.075)
        borefield.calculate_temperatures(circle_field.depth_max)
        li.append((n_1, np.max(borefield.results_peak_cooling) - borefield.Tf_max, np.min(borefield.results_peak_heating) - borefield.Tf_min))
        if np.max(borefield.results_peak_cooling) <= borefield.Tf_max and np.min(borefield.results_peak_heating) >= borefield.Tf_min:
            n_min_manual = n_1
    pd.DataFrame(li).to_csv("test.csv")
    print(n_min_manual)  # """
    assert min_number == 55

    configs = size_borefield(borefield, check_configs=True)
    assert borefield.number_of_boreholes == configs[0][1]
    min_number = borefield.number_of_boreholes
    assert min_number == 55
