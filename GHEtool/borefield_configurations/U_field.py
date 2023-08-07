import math

import pygfunction as gt

from GHEtool.borefield_configurations.borefield_configuration import BorefieldConfiguration


class UField(BorefieldConfiguration):

    def __init__(self, N_1: int, N_2: int, B_1: float, B_2: float, H: float, D: float, r_b: float):
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

        self.li_boreholes: list[gt.boreholes.Borehole] = gt.boreholes.U_shaped_field(N_1, N_2, B_1, B_2, H, D, r_b)
        self.H: float = H
        self.D: float = D
        self.r_b: float = r_b
        self.depth_max: float = 100.
        self.max_length_x: float = 100.
        self.max_length_y: float = 100.

    def create_start_config(self) -> list[tuple[float, int, int, float, float]]:
        self.li_boreholes = gt.boreholes.U_shaped_field(2, 2, self.max_length_x, self.max_length_y, self.depth_max, self.D, self.r_b)
        return [(self.depth_max, 2, 2, self.max_length_x, self.max_length_y)]

    def update_config(self, n_min: int) -> list[tuple[float, int, int, float, float]]:
        configs = []
        n_min_loop = int(self.max_length_x) + (int(self.max_length_y) - 1)
        if n_min > 2*(int(self.max_length_x) + 1) + (int(self.max_length_y) - 1):
            configs = [(self.depth_max, int(self.max_length_x) + 1, int(self.max_length_y) + 1, self.max_length_x / ((int(self.max_length_x) + 1) - 1),
                        self.max_length_y / ((int(self.max_length_y) + 1) - 1))]
            self.reset_from_config(configs[0])
            return configs
        for n_x in range(2, int(self.max_length_x) + 2):
            n_w_start = int(n_x / self.max_length_y)
            if math.ceil(n_w_start + n_x - 1) > n_min or n_w_start > int(self.max_length_y):
                continue
            for n_y in range(max(int(n_x / self.max_length_y), 2), int(self.max_length_y) + 2):
                n_boreholes = (2*n_y + n_x - 2)
                if n_boreholes > n_min_loop or n_boreholes< n_min:
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
