import pygfunction as gt

from GHEtool.borefield_configurations.borefield_configuration import BorefieldConfiguration


class UndefinedBorefield(BorefieldConfiguration):

    def __init__(self, borefield: list[gt.boreholes.Borehole]):
        self.li_boreholes: list[gt.boreholes.Borehole] = borefield
        self.H: float = borefield[0].H
        self.D: float = borefield[0].D
        self.r_b: float = borefield[0].r_b
        self.depth_max: float = 100.

    def create_start_config(self) -> tuple:
        raise NotImplementedError

    def update_config(self, n_min: int) -> list[tuple]:
        raise NotImplementedError

    def reset_from_config(self, config: tuple):
        raise NotImplementedError