import math

import pygfunction as gt

from GHEtool.borefield_configurations.borefield_configuration import BorefieldConfiguration


class UField(BorefieldConfiguration):

    def __init__(self, n_x: int, n_y: int, b_x: float, b_y: float, depth: float, buried_depth: float, radius_borehole: float):
        """
        This function creates a U shaped borefield.
        It calls the pygfunction module in the background.
        The documentation of this function is based on pygfunction.
        x-> y^
        o    o
        o    o
        o    o
        oooooo
        -> N_1 = 6, N_2 =4

        Parameters
        ----------
        n_x : int
            Number of boreholes in the x direction
        n_y : int
            Number of boreholes in the y direction
        b_x : float
            Distance between adjacent boreholes in the x direction [m]
        b_y : float
            Distance between adjacent boreholes in the y direction [m]
        depth : float
            Borehole depth [m]
        buried_depth : float
            Borehole buried depth [m]
        radius_borehole : float
            Borehole radius [m]



        """

        self.li_boreholes: list[gt.boreholes.Borehole] = gt.boreholes.U_shaped_field(n_x, n_y, b_x, b_y, depth, buried_depth, radius_borehole)
        self.H: float = depth
        self.D: float = buried_depth
        self.r_b: float = radius_borehole
        self.depth_max: float = 100.
        self.max_length_x: float = 100.
        self.max_length_y: float = 100.
        self.min_distance: float = 1.

    def create_start_config(self) -> list[tuple[float, int, int, float, float]]:
        self.li_boreholes = gt.boreholes.U_shaped_field(2, 2, self.max_length_x, self.max_length_y, self.depth_max, self.D, self.r_b)
        return [(self.depth_max, 2, 2, self.max_length_x, self.max_length_y)]

    def update_config(self, n_min: int) -> list[tuple[float, int, int, float, float]]:
        configs = []
        n_min_loop = int(self.max_length_x / self.min_distance) + 2 * int(self.max_length_y / self.min_distance) - 2
        if n_min >= (int(self.max_length_x / self.min_distance) + 1) + 2 * (int(self.max_length_y / self.min_distance) + 1) - 2:
            configs = [(self.depth_max, int(self.max_length_x / self.min_distance) + 1, int(self.max_length_y / self.min_distance) + 1,
                        self.max_length_x / (int(self.max_length_x / self.min_distance) + 1),
                        self.max_length_y / (int(self.max_length_y / self.min_distance) + 1))]
            self.reset_from_config(configs[0])
            return configs
        for n_x in range(2, int(self.max_length_x / self.min_distance) + 2):
            n_y_start = int(n_min * 0.5 + 1 - n_x * 0.5)
            if math.ceil(n_y_start + n_x - 1) > n_min or n_y_start > int(self.max_length_y / self.min_distance):
                continue
            for n_y in range(max(int(n_x / self.max_length_y), 2), int(self.max_length_y / self.min_distance) + 2):
                n_boreholes = 2 * n_y + n_x - 2
                if n_boreholes > n_min_loop or n_boreholes < n_min:
                    continue
                if n_boreholes < n_min_loop:
                    configs = []
                n_min_loop = n_boreholes
                configs.append((self.depth_max, n_x, n_y, self.max_length_x / (n_x - 1), self.max_length_y / (n_y - 1)))
        configs = sorted(configs, key=lambda x: abs(x[3] - x[4]))
        self.reset_from_config(configs[0])
        return configs

    def reset_from_config(self, config: tuple[float, int, int, float, float]):
        self.li_boreholes = gt.boreholes.U_shaped_field(config[1], config[2], config[3], config[4], self.depth_max, self.D, self.r_b)
