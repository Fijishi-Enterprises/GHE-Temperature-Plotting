import math

import pygfunction as gt

from GHEtool.borefield_configurations.borefield_configuration import BorefieldConfiguration


class CircleField(BorefieldConfiguration):

    def __init__(self, n: int, radius_center_2_boreholes: float, H: float, D: float, r_b: float):
        """
        This function creates a circle shaped borefield.
        It calls the pygfunction module in the background.
        The documentation of this function is based on pygfunction.

        Parameters
        ----------
        n : int
            Number of boreholes
        radius_center_2_boreholes : float
            radius form center to boreholes
        H : float
            Borehole depth [m]
        D : float
            Borehole buried depth [m]
        r_b : float
            Borehole radius [m]
        """

        self.li_boreholes: list[gt.boreholes.Borehole] = gt.boreholes.circle_field(n, radius_center_2_boreholes, H, D, r_b)
        self.H: float = H
        self.D: float = D
        self.r_b: float = r_b
        self.depth_max: float = 100.
        self.max_radius_center_2_boreholes: float = 100.
        self.min_distance: float = 1.

    def create_start_config(self) -> list[tuple[float, int, float]]:
        self.li_boreholes = gt.boreholes.circle_field(2, self.max_radius_center_2_boreholes, self.depth_max, self.D, self.r_b)
        return [(self.depth_max, 2, self.max_radius_center_2_boreholes)]

    def update_config(self, n_min: int) -> list[tuple[float, int, float]]:
        configs = []
        n = int(4*math.pi * self.max_radius_center_2_boreholes/self.min_distance)
        if n_min > n:
            configs = [(self.depth_max, n, self.max_radius_center_2_boreholes)]
            self.reset_from_config(configs[0])
            return configs
        configs = [(self.depth_max, n_min, self.max_radius_center_2_boreholes)]
        self.reset_from_config(configs[0])
        return configs

    def reset_from_config(self, config: tuple[float, int, float]):
        self.li_boreholes = gt.boreholes.circle_field(config[1], config[2], self.depth_max, self.D, self.r_b)
