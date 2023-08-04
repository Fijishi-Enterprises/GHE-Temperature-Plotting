import math

import numpy as np

from GHEtool import Borefield

class NoBorefieldFoundError(Exception):
    def __init__(self):
        super().__init__("No Borefield configuration found")


def size_borefield(borefield: Borefield, *, check_configs: bool = False) -> list[tuple]:
    configs = []
    max_depth = borefield.borefield.depth_max
    best_config: tuple[list[tuple], int] = (borefield.create_start_config(), 1_000_000)
    borefield.calculate_temperatures(max_depth)
    H_cool = (np.max(borefield.results_peak_cooling) - borefield._Tg()) / (borefield.Tf_max - borefield._Tg()) * max_depth * borefield.number_of_boreholes
    H_heat = (np.min(borefield.results_peak_heating) - borefield._Tg()) / (borefield.Tf_min - borefield._Tg()) * max_depth * borefield.number_of_boreholes
    if max(H_cool, H_heat) <= max_depth:
        return best_config[0]
    n = max(H_cool, H_heat) / max_depth
    config = borefield.update_config(n)
    borefield.calculate_temperatures(max_depth)
    H_cool = (np.max(borefield.results_peak_cooling) - borefield._Tg()) / (borefield.Tf_max - borefield._Tg()) * max_depth * borefield.number_of_boreholes
    H_heat = (np.min(borefield.results_peak_heating) - borefield._Tg()) / (borefield.Tf_min - borefield._Tg()) * max_depth * borefield.number_of_boreholes
    configs.append(config)
    if max(H_heat, H_cool) <= max_depth * borefield.number_of_boreholes:
        best_config = (configs[-1], borefield.number_of_boreholes)

    while configs[-1] not in configs[:-1]:
        n = max(H_cool, H_heat) / max_depth
        config = borefield.update_config(n)
        borefield.calculate_temperatures(max_depth)
        H_cool = (np.max(borefield.results_peak_cooling) - borefield._Tg()) / (borefield.Tf_max - borefield._Tg()) * max_depth * borefield.number_of_boreholes
        H_heat = (np.min(borefield.results_peak_heating) - borefield._Tg()) / (borefield.Tf_min - borefield._Tg()) * max_depth * borefield.number_of_boreholes
        configs.append(config)
        if max(H_heat, H_cool) <= max_depth * borefield.number_of_boreholes and borefield.number_of_boreholes < best_config[1]:
            best_config = (config, borefield.number_of_boreholes)
            continue
        if not(max_depth * 0.9 <= max(H_heat, H_cool) / borefield.number_of_boreholes <= max_depth * 1.1):
            continue
        other_configs = [conf for conf in config[1:] if borefield.check_config(conf)]
        if other_configs:
            borefield.borefield.reset_from_config(other_configs[0])
            borefield.calculate_temperatures(max_depth)
            H_cool = (
                (np.max(borefield.results_peak_cooling) - borefield._Tg()) / (borefield.Tf_max - borefield._Tg()) * max_depth * borefield.number_of_boreholes
            )
            H_heat = (
                (np.min(borefield.results_peak_heating) - borefield._Tg()) / (borefield.Tf_min - borefield._Tg()) * max_depth * borefield.number_of_boreholes
            )
            best_config = (other_configs, borefield.number_of_boreholes)

    for n in range(best_config[1], max(int(best_config[1] * 0.9), best_config[1] - 5), -1):
        config = borefield.update_config(n)
        if borefield.number_of_boreholes >= best_config[1]:
            continue
        other_configs = [conf for conf in config[1:] if borefield.check_config(conf)]
        if other_configs:
            best_config = (other_configs, borefield.number_of_boreholes)
            continue

    if check_configs:
        best_config = ([config for config in best_config[0] if borefield.check_config(config)], best_config[1])
    if best_config[0] == [] or best_config == (borefield.create_start_config(), 1_000_000):
        raise NoBorefieldFoundError
    return best_config[0]
