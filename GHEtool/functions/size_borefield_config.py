import math

import numpy as np

from GHEtool import Borefield


def size_borefield(borefield: Borefield, *, check_configs: bool = False) -> list[tuple]:
    configs = []
    max_depth = borefield.borefield.depth_max
    best_config = (borefield.create_start_config(), 1_000_000)
    borefield.calculate_temperatures(max_depth)
    H_cool = (np.max(borefield.results_peak_cooling) - borefield._Tg()) / (borefield.Tf_max - borefield._Tg()) * max_depth * borefield.number_of_boreholes
    H_heat = (np.min(borefield.results_peak_heating) - borefield._Tg()) / (borefield.Tf_min - borefield._Tg()) * max_depth * borefield.number_of_boreholes
    if max(H_cool, H_heat) <= max_depth:
        return [best_config[0]]
    n = math.ceil(max(H_cool, H_heat) / max_depth)
    config = borefield.update_config(n)
    borefield.calculate_temperatures(max_depth )
    H_cool = (np.max(borefield.results_peak_cooling) - borefield._Tg()) / (borefield.Tf_max - borefield._Tg()) * max_depth * borefield.number_of_boreholes
    H_heat = (np.min(borefield.results_peak_heating) - borefield._Tg()) / (borefield.Tf_min - borefield._Tg()) * max_depth * borefield.number_of_boreholes
    configs.append(config)
    if max(H_heat, H_cool) <= max_depth * borefield.number_of_boreholes:
        best_config = (configs[-1], borefield.number_of_boreholes)

    while configs[-1] not in configs[:-1]:
        n = math.ceil(max(H_cool, H_heat) / max_depth)
        config = borefield.update_config(n)
        borefield.calculate_temperatures(max_depth)
        H_cool = (np.max(borefield.results_peak_cooling) - borefield._Tg()) / (borefield.Tf_max - borefield._Tg()) * max_depth * borefield.number_of_boreholes
        H_heat = (np.min(borefield.results_peak_heating) - borefield._Tg()) / (borefield.Tf_min - borefield._Tg()) * max_depth * borefield.number_of_boreholes
        configs.append(config)
        if max(H_heat, H_cool) <= max_depth * borefield.number_of_boreholes and borefield.number_of_boreholes < best_config[1]:
            best_config = (configs[-1], borefield.number_of_boreholes)

    if check_configs:
        best_config = ([config for config in best_config[0] if borefield.check_config(config)], best_config[1])


    return best_config[0]
