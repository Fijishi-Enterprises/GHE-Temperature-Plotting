"""
This document contains the class for the double U-Pipe borehole.
"""

from GHEtool.VariableClasses.PipeData.MultipleUTube import MultipleUTube


class DoubleUPipe(MultipleUTube):
    """
    Class for the double U-Pipe borehole.
    """
    def __init__(self, k_g: float = None,
                 r_in: float = None,
                 r_out: float = None,
                 k_p: float = None,
                 D_s: float = None,
                 epsilon: float = 1e-6):
        """

        Parameters
        ----------
        k_g : float
            Grout thermal conductivity [W/mK]
        r_in : float
            Inner pipe radius [m]
        r_out : float
            Outer pipe radius [m]
        k_p : float
            Pipe thermal conductivity [W/mK]
        D_s : float
            Distance of the pipe until center [m]
        epsilon : float
            Pipe roughness [m]
        """
        super().__init__(k_g, r_in, r_out, k_p, D_s, 2, epsilon)