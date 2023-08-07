import numpy as np

from GHEtool import Borefield, GroundConstantTemperature, MonthlyGeothermalLoadAbsolute
from GHEtool.functions.size_borefield_config import size_borefield


def main():
    # relevant borefield data for the calculations
    data = GroundConstantTemperature(
        3, 10, 2.4 * 10**6  # conductivity of the soil (W/mK)  # Ground temperature at infinity (degrees C)
    )  # ground volumetric heat capacity (J/m3K)

    # monthly loading values
    peak_cooling = np.array([0.0, 0, 34.0, 69.0, 133.0, 187.0, 213.0, 240.0, 160.0, 37.0, 0.0, 0.0])  # Peak cooling in kW
    peak_heating = np.array([160.0, 142, 102.0, 55.0, 0.0, 0.0, 0.0, 0.0, 40.4, 85.0, 119.0, 136.0])  # Peak heating in kW

    # annual heating and cooling load
    annual_heating_load = 300 * 10**3  # kWh
    annual_cooling_load = 160 * 10**3  # kWh

    # percentage of annual load per month (15.5% for January ...)
    monthly_load_heating_percentage = np.array([0.155, 0.148, 0.125, 0.099, 0.064, 0.0, 0.0, 0.0, 0.061, 0.087, 0.117, 0.144])
    monthly_load_cooling_percentage = np.array([0.025, 0.05, 0.05, 0.05, 0.075, 0.1, 0.2, 0.2, 0.1, 0.075, 0.05, 0.025])

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
    rect_field = borefield.create_rectangular_borefield(16, 8, 30 / 15, 20 / 7, 95, 4, 0.075)
    # borefield.calculate_temperatures(95)
    # borefield.print_temperature_profile()
    rect_field.max_length = 30
    rect_field.max_width = 20
    rect_field.depth_max = 95

    borefield.Rb = 0.12  # equivalent borehole resistance (K/W)

    # set temperature boundaries
    borefield.set_max_ground_temperature(16)  # maximum temperature
    borefield.set_min_ground_temperature(0)  # minimum temperature
    """
    configs = size_borefield(borefield)
    print("The possible configurations are:")
    for config in configs:
        print(f"depth: {config[0]}, boreholes length: {config[1]}, boreholes width: {config[2]}, spacing length {config[3]}, spacing width {config[4]}")
    configs = size_borefield(borefield, check_configs=True)
    print("The possible configurations which fits the demand are:")
    for config in configs:
        print(f"depth: {config[0]}, boreholes length: {config[1]}, boreholes width: {config[2]}, spacing length {config[3]}, spacing width {config[4]}")"""
    # borefield.calculate_temperatures(rect_field.depth_max)
    # borefield.print_temperature_profile()
    """
    box_field = borefield.create_box_borefield(16, 8, 30 / 15, 20 / 7, 95, 4, 0.075)
    # borefield.calculate_temperatures(95)
    # borefield.print_temperature_profile()
    box_field.max_length = 40
    box_field.max_width = 50
    box_field.depth_max = 95
    configs = size_borefield(borefield)
    print("The possible configurations are:")
    for config in configs:
        print(f"depth: {config[0]}, boreholes length: {config[1]}, boreholes width: {config[2]}, spacing length {config[3]}, spacing width {config[4]}")
    configs = size_borefield(borefield, check_configs=True)
    print("The possible configurations which fits the demand are:")
    for config in configs:
        print(f"depth: {config[0]}, boreholes length: {config[1]}, boreholes width: {config[2]}, spacing length {config[3]}, spacing width {config[4]}")
    
    l_field = borefield.create_L_shaped_borefield(16, 8, 30 / 15, 20 / 7, 95, 4, 0.075)
    # borefield.calculate_temperatures(95)
    # borefield.print_temperature_profile()
    l_field.max_length = 50
    l_field.max_width = 60
    l_field.depth_max = 150
    configs = size_borefield(borefield)
    print("The possible configurations which fits the demand are:")
    for config in configs:
        print(f"depth: {config[0]}, boreholes length: {config[1]}, boreholes width: {config[2]}, spacing length {config[3]}, spacing width {config[4]}")
    """
    """
    u_field = borefield.create_U_shaped_borefield(16, 8, 30 / 15, 20 / 7, 95, 4, 0.075)
    # borefield.calculate_temperatures(95)
    # borefield.print_temperature_profile()
    u_field.max_length_x = 50
    u_field.max_length_y = 60
    u_field.depth_max = 150
    configs = size_borefield(borefield, check_configs=True)
    print("The possible configurations which fits the demand are:")
    for config in configs:
        print(f"depth: {config[0]}, boreholes length: {config[1]}, boreholes width: {config[2]}, spacing length {config[3]}, spacing width {config[4]}")"""

    circle_field = borefield.create_circular_borefield(16, 9, 95, 4, 0.075)
    # borefield.calculate_temperatures(95)
    # borefield.print_temperature_profile()
    circle_field.max_radius_center_2_boreholes = 50
    circle_field.depth_max = 150
    configs = size_borefield(borefield)
    print("The possible configurations which fits the demand are:")
    for config in configs:
        print(f"depth: {config[0]}, number boreholes: {config[1]}")


if __name__ == "__main__":  # pragma: no cover
    main()
