import math

import pygfunction as gt

from GHEtool.borefield_configurations.borefield_configuration import BorefieldConfiguration


class BoxField(BorefieldConfiguration):

    def __init__(self, N_1: int, N_2: int, B_1: float, B_2: float, H: float, D: float, r_b: float):
        """
        This function creates a box borefield.
        It calls the pygfunction module in the background.
        The documentation of this function is based on pygfunction.

        Parameters
        ----------
        N_1 : int
            Number of boreholes in the x direction
        N_2 : int
            Number of boreholes in the y direction
        B_1 : float
            Distance between adjacent boreholes in the x direction [m]
        B_2 : float
            Distance between adjacent boreholes in the y direction [m]
        H : float
            Borehole depth [m]
        D : float
            Borehole buried depth [m]
        r_b : float
            Borehole radius [m]
        """

        self.li_boreholes: list[gt.boreholes.Borehole] = gt.boreholes.box_shaped_field(N_1, N_2, B_1, B_2, H, D, r_b)
        self.H: float = H
        self.D: float = D
        self.r_b: float = r_b
        self.depth_max: float = 100.
        self.max_length: float = 100.
        self.max_width: float = 100.

    def create_start_config(self) -> list[tuple[float, int, int, float, float]]:
        self.li_boreholes = gt.boreholes.box_shaped_field(2, 2, self.max_length, self.max_width, self.depth_max, self.D, self.r_b)
        return [(self.depth_max, 2, 2, self.max_length, self.max_width)]

    def update_config(self, n_min: int) -> list[tuple[float, int, int, float, float]]:
        configs = []
        n_min_loop = 2 * int(self.max_length) + 2 * (int(self.max_width) - 2)
        if n_min > (int(self.max_length) + 1) * 2 + 2 * (int(self.max_width) - 1):
            configs = [(self.depth_max, int(self.max_length) + 2, int(self.max_width) + 2, self.max_length / ((int(self.max_length) + 2) - 1),
                        self.max_width / ((int(self.max_width) + 2) - 1))]
            self.reset_from_config(configs[0])
            return configs
        for n_l in range(2, int(self.max_length) + 2):
            n_w_start = int(n_l / self.max_width)
            if math.ceil(2 * n_w_start + 2 * (n_l - 2)) > n_min or n_w_start > int(self.max_width):
                continue
            for n_w in range(max(int(n_l / self.max_width), 2), int(self.max_width) + 2):
                if (2 * n_w + 2 * (n_l - 2)) > n_min_loop or (2 * n_w + 2 * (n_l - 2)) < n_min:
                    continue
                if (2 * n_w + 2 * (n_l - 2)) < n_min_loop:
                    configs = []
                n_min_loop = 2 * n_w + 2 * (n_l - 2)
                configs.append((self.depth_max, n_l, n_w, self.max_length / (n_l - 1), self.max_width / (n_w - 1)))
        configs = sorted(configs, key=lambda x: abs(x[3] - x[4]))
        self.reset_from_config(configs[0])
        return configs

    def reset_from_config(self, config: tuple[float, int, int, float, float]):
        self.li_boreholes = gt.boreholes.box_shaped_field(config[1], config[2], config[3], config[4], self.depth_max, self.D, self.r_b)
