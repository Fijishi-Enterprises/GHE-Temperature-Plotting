"""
Test to see if the Rb* is calculated on the go
"""
import sys
from pathlib import Path
from typing import Tuple

import numpy as np
import PySide6.QtWidgets as QtW
import pandas as pd

from GHEtool import Borefield, FOLDER, FluidData, GroundConstantTemperature, GroundFluxTemperature, PipeData, GroundTemperatureGradient
from GHEtool.gui.data_2_borefield_func import data_2_borefield
from GHEtool.gui.gui_classes.gui_combine_window import MainWindow
from GHEtool.gui.gui_classes.translation_class import Translations
from GHEtool.gui.gui_structure import GUI, GuiStructure
from ScenarioGUI import load_config
import pygfunction as gt

load_config(Path(__file__).parent.parent.joinpath("gui_config.ini"))

sys.setrecursionlimit(1500)


def test_Rb_calculated_when_value_changed(qtbot):
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=Borefield,
                             data_2_results_function=data_2_borefield)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=Borefield,
                             data_2_results_function=data_2_borefield)
    main_window.save_scenario()

    gs = main_window.gui_structure
    assert gs.pipe_thermal_resistance.is_hidden()

    gs.option_method_rb_calc.set_value(1)
    gs.page_borehole_resistance.button.click()
    assert not gs.pipe_thermal_resistance.is_hidden()
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 100.0m): 0.0579 mK/W'
    gs.option_conductivity.set_value(2.5)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 100.0m): 0.058 mK/W'
    gs.option_depth.set_value(160)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0686 mK/W'
    gs.option_fluid_conductivity.set_value(0.6)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0684 mK/W'
    gs.option_fluid_density.set_value(2000)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0684 mK/W'
    gs.option_fluid_capacity.set_value(4000)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.07 mK/W'
    gs.option_fluid_viscosity.set_value(0.002)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.071 mK/W'
    gs.option_fluid_mass_flow.set_value(0.6)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.065 mK/W'
    gs.option_pipe_number.set_value(1)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0839 mK/W'
    gs.option_pipe_grout_conductivity.set_value(1.6)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0806 mK/W'
    gs.option_pipe_conductivity.set_value(0.44)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0798 mK/W'
    gs.option_pipe_inner_radius.set_value(0.021)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0709 mK/W'
    gs.option_pipe_outer_radius.set_value(0.023)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0769 mK/W'
    gs.option_pipe_borehole_radius_2.set_value(0.076)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0783 mK/W'
    gs.option_pipe_distance.set_value(0.041)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.077 mK/W'
    gs.option_pipe_roughness.set_value(0.00002)
    assert gs.pipe_thermal_resistance.label.text() == 'The equivalent borehole thermal resistance (at 160.0m): 0.0769 mK/W'
