import math

import pygfunction as gt

from GHEtool.borefield_configurations.borefield_configuration import BorefieldConfiguration


class RectangularField(BorefieldConfiguration):

    def __init__(self, N_1, N_2, B_1, B_2, H, D, r_b):
        """
        This function creates a rectangular borefield.
        It calls the pygfunction module in the background.
        The documentation of this function is based on pygfunction.

        Parameters
        ----------
        N_1 : int
            Number of boreholes in the x direction
        N_2 : int
            Number of boreholes in the y direction
        B_1 : int
            Distance between adjacent boreholes in the x direction [m]
        B_2 : int
            Distance between adjacent boreholes in the y direction [m]
        H : float
            Borehole depth [m]
        D : float
            Borehole buried depth [m]
        r_b : float
            Borehole radius [m]
        """

        self.li_boreholes: list[gt.boreholes.Borehole] = gt.boreholes.rectangle_field(N_1, N_2, B_1, B_2, H, D, r_b)
        self.H: float = H
        self.D: float = D
        self.r_b: float = r_b
        self.depth_max: float = 100.
        self.max_length: float = 100.
        self.max_width: float = 100.

    def create_start_config(self) -> list[tuple[float, int, int, float, float]]:
        self.li_boreholes = gt.boreholes.rectangle_field(2, 2, self.max_length, self.max_width, self.depth_max, self.D, self.r_b)
        return [(self.depth_max, 2, 2, self.max_length, self.max_width)]

    def update_config(self, n_min: int) -> list[tuple[float, int, int, float, float]]:
        configs = []
        n_min_loop = 2 * 2 * int(self.max_width) * int(self.max_length)
        if n_min > (int(self.max_length) + 2) * (int(self.max_width) + 2):
            configs = [(self.depth_max, int(self.max_length) + 2, int(self.max_width) + 2, self.max_length / ((int(self.max_length) + 2) - 1),
                       self.max_width / ((int(self.max_width) + 2) - 1))]
            self.reset_from_config(configs[0])
            return configs
        for n_l in range(2, int(self.max_length) + 2):
            n_w_start = int(n_l / self.max_width)
            if math.ceil(n_w_start * n_l) > n_min or n_w_start > int(self.max_width):
                continue
            for n_w in range(max(int(n_l / self.max_width), 2), int(self.max_width) + 2):
                if n_w * n_l > n_min_loop or n_w * n_l < n_min:
                    continue
                if n_w * n_l < n_min_loop:
                    configs = []
                n_min_loop = n_w * n_l
                configs.append((self.depth_max, n_l, n_w, self.max_length / (n_l - 1), self.max_width / (n_w - 1)))
        configs = sorted(configs, key=lambda x: abs(x[3] - x[4]))
        self.reset_from_config(configs[0])
        return configs
    
    def reset_from_config(self, config: tuple[float, int, int, float, float]):
        self.li_boreholes = gt.boreholes.rectangle_field(config[1], config[2], config[3], config[4], self.depth_max, self.D, self.r_b)
