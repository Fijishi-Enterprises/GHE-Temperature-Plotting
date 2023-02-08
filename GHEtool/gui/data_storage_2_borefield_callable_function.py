from functools import partial
from typing import Callable, Tuple

from GHEtool import Borefield
from GHEtool.gui.gui_data_storage import DataStorage
from GHEtool.gui.gui_structure import load_data_GUI


def data_storage_2_borefield_callable(ds: DataStorage) -> Tuple[Borefield, Callable[[], None]]:
    # import bore field class from GHEtool and not in start up to save time
    from GHEtool import Borefield


    # create the bore field object
    borefield = Borefield(
        simulation_period=ds.option_simu_period,
        borefield=ds.borefield_pygfunction,
        gui=True,
    )
    # set temperature boundaries
    borefield.set_max_ground_temperature(ds.option_max_temp)  # maximum temperature
    borefield.set_min_ground_temperature(ds.option_min_temp)  # minimum temperature

    # set ground data
    borefield.set_ground_parameters(ds.ground_data)

    # set peak lengths
    borefield.set_length_peak_cooling(ds.option_len_peak_cooling)
    borefield.set_length_peak_heating(ds.option_len_peak_heating)

    ### GENERAL SETUPS

    # check if Rb is a constant, otherwise set the fluid/pipe parameters
    if ds.option_method_rb_calc > 0:
    # Rb will be dynamically calculated
    # set fluid and pipe data
        borefield.set_fluid_parameters(ds.fluid_data)
    borefield.set_pipe_parameters(ds.pipe_data)

    # set monthly loads
    borefield.set_peak_heating(ds.peakHeating)
    borefield.set_peak_cooling(ds.peakCooling)
    borefield.set_baseload_heating(ds.monthlyLoadHeating)
    borefield.set_baseload_cooling(ds.monthlyLoadCooling)

    # set hourly loads if available
    if ds.hourly_data:
        data_unit = ds.option_unit_data

        peak_heating, peak_cooling = load_data_GUI(
            filename=ds.option_filename,
            thermal_demand=ds.option_column,
            heating_load_column=ds.option_heating_column_text,
            cooling_load_column=ds.option_cooling_column_text,
            combined=ds.option_single_column_text,
            sep=";" if ds.option_seperator_csv == 0 else ",",
            dec="." if ds.option_decimal_csv == 0 else ",",
            fac=0.001 if data_unit == 0 else 1 if data_unit == 1 else 1000,
            hourly=True)

        # hourly data to be loaded
        borefield.set_hourly_heating_load(peak_heating)
        borefield.set_hourly_cooling_load(peak_cooling)

    # set up the borefield sizing
    borefield.sizing_setup(H_init=ds.borefield_pygfunction[0].H,
                           use_constant_Rb=ds.option_method_rb_calc == 0,
                           use_constant_Tg=ds.option_method_temp_gradient == 0,
                           L2_sizing=ds.option_method_size_depth == 0,
                           L3_sizing=ds.option_method_size_depth == 1,
                           L4_sizing=ds.option_method_size_depth == 2)

    ### FUNCTIONALITIES (i.e. aims)

    # if load should be optimized do this
    if ds.aim_optimize:
        # optimize load profile without printing the results
        return borefield, partial(borefield.optimise_load_profile)

            ### Size borefield
    if ds.aim_req_depth:
        return borefield, partial(borefield.size)


        ### Size borefield by length and width
        # if ds.aim_size_length:
        #     try:
        #         # To be implemented
        #         # option_method_size_length
        #         pass
        #     except RuntimeError or ValueError:
        #         # save bore field in Datastorage
        #         ds.borefield = None
        #         # return Datastorage as signal
        #         self.any_signal.emit((ds, self.idx))
        #         return

        ### Plot temperature profile
    if ds.aim_temp_profile:
        return borefield, partial(borefield.calculate_temperatures, borefield.H)