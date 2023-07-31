import abc

import pygfunction as gt

class BorefieldConfiguration:

    li_boreholes: list[gt.boreholes.Borehole]
    H: float
    D: float
    r_b: float
    depth_max: float

    @abc.abstractmethod
    def create_start_config(self) -> tuple:
        """"""

    @abc.abstractmethod
    def update_config(self, n_min: int) -> list[tuple]:
        """"""

    @abc.abstractmethod
    def reset_from_config(self, config: tuple):
        """"""