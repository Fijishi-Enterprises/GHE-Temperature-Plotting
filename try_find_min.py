import numpy as np
from GHEtool import Borefield


def size_by_length_and_width(borefield: Borefield, H_max: float, L1: float, L2: float, B_min: float = 3.0,
                             B_max: float = 9.0, L2_sizing: bool = True, nb_of_options: int = 5) -> list:
    """
    Function to size the borefield by length and with. It returns a list of possible borefield sizes,
    with increasing total length.
    :param H_max: maximal borehole depth [m]
    :param L1: maximal width of borehole field [m]
    :param L2: maximal length of borehole field [m]
    :param B_min: minimal borehole spacing [m]
    :param B_max: maximal borehole spacing [m]
    :param L2_sizing: boolean to check if level two or level three sizing method should be used
    :param nb_of_options: number of options that should be returned.
    :return: list of possible combinations (each combination is a tuple where the first two elements are the
    number of boreholes in each direction, the third element the borehole spacing and the fourth element
    the depth of the borefield and the last element is the total borefield length).
    An Empty list is returned if no result is found
    """

    # set larger one of l_1 and l_2 to the width
    max_width = max(L1, L2)
    max_length = min(L1, L2)

    # calculate max borefield size
    N1_max = min(int(max_width / B_min), 20)
    N2_max = min(int(max_length / B_min), 20)

    # set depth to maximum depth
    borefield.H = H_max

    # calculate set of possible options
    options = set([])
    for N1 in range(1, N1_max + 1):
        for N2 in range(N1, N2_max + 1):
            # calculate possible spacings
            B = min(max_width / N1, max_length / N2, B_max)

            # iterate over all possible B's
            for B in np.arange(B_min, B + 0.1, 0.5):
                # set borefield parameters
                borefield.create_rectangular_borefield(N1, N2, B, B, H_max, borefield.borefield[0].D, borefield.borefield[0].r_b)
                borefield.calculate_temperatures(H_max)
                if np.max(borefield.results_peak_cooling) <= borefield.Tf_max and np.min(borefield.results_peak_heating) >= borefield.Tf_min:
                    options.add((N1, N2, B))
                    break

    # return empty list if options = {}
    if options == set([]):
        return []

    # set result dictionary
    results = {}

    # size all options
    for option in options:
        borefield._reset_for_sizing(option[0], option[1])
        borefield.B = option[2]
        depth = borefield.size(H_init=100, L2_sizing=L2_sizing)

        # save result in results dictionary with the total length as key
        results[depth * borefield.number_of_boreholes] = (option[0], option[1], option[2], depth)

    # get all the solutions
    lengths = list(results.keys())
    lengths.sort()
    # reverse for decending order
    lengths[::-1]

    # cut to right length
    lengths = lengths[0:nb_of_options]

    return [results[i] for i in lengths]


def size_complete_field_robust(borefield: Borefield, H_max: float, l_1: float, l_2: float, B_min: float = 3.0, B_max: float = 9.0,
                               L2_sizing: bool = True, use_constant_Rb: bool = False) -> list:
    """
    Function to size the minimal number of borefield by borefield length and width on a robust and more
    time-consuming way.
    :param H_max: maximal borehole depth [m]
    :param l_1: maximal width of borehole field [m]
    :param l_2: maximal length of borehole field [m]
    :param B_min: minimal borehole spacing [m]
    :param B_max: maximal borehole spacing [m]
    :param L2_sizing: boolean to check if level two or level three sizing method should be used
    :param use_constant_Rb: boolean to check if a constant borehole resistance should be used
    :return: list of possible combinations (each combination is a tuple where the first two elements are the
    number of boreholes in each direction, the third element the borehole spacing and the last element
    the depth of the borefield). An Empty list is returned if no result is found
    """
    # check if length > width
    l_2_bigger_then_l_1: bool = l_2 > l_1
    # change length and width if length > width
    (l_1, l_2) = (l_2, l_1) if l_2_bigger_then_l_1 else (l_1, l_2)
    # set start maximal number of boreholes
    n_n_max_start: int = 20 * 20
    # set maximal number of boreholes
    n_n_max: int = n_n_max_start
    # list of possible combinations
    combo: list = []
    # minimal product to break loop
    product_min = 0
    # start loop over borehole spacing
    for B in np.arange(B_max, B_min * 0.99999, -0.5):
        # calculate maximal number of boreholes in length and width direction
        n_1_max = min(int(l_1 / B), 20)
        n_2_max = min(int(l_2 / B), 20)
        # set borehole spacing
        borefield.B = B
        # start loop over number of boreholes in length and width direction
        for N_1 in range(n_1_max, 0, -1):
            for N_2 in range(min(n_2_max, N_1), 0, -1):
                # reset borefield values for sizing
                borefield._reset_for_sizing(N_1, N_2)
                # calculate number of total boreholes which should be minimal
                product = N_1 * N_2
                # continue loop if product is higher than current maxima to avoid calculation
                if product > n_n_max:
                    continue
                # break loop id product is less than the current minima to avoid calculation
                if product < product_min:
                    break
                # try to size current borefield configuration else set minimal product
                try:
                    depth = borefield.size(H_max, L2Sizing=L2_sizing, L3_sizing=not L2_sizing, use_constant_Rb=use_constant_Rb)
                except ValueError:
                    product_min = product
                    continue
                # break loop if depth is higher than the maxima
                if depth > H_max:
                    break
                # save result in combo list and update maximal number of boreholes if current product is less the
                # maxima
                if product < n_n_max:
                    n_n_max = product
                    combo = [[N_1, N_2, B, depth]]
                # append solution which leads to the same number of boreholes
                elif product == n_n_max:
                    combo.append([N_1, N_2, B, depth])
    # if no solution is found return an empty list
    if n_n_max == n_n_max_start:
        return []
    # change N_1 and N_2 if length > width
    combo = [[i[1], i[0], i[2], i[3]] for i in combo] if l_2_bigger_then_l_1 else combo
    # set number of boreholes in length and width, borehole spacing and depth of first solution
    borefield.N_1 = combo[0][0]
    borefield.N_2 = combo[0][1]
    borefield.B = combo[0][2]
    borefield.H = combo[0][3]
    # reset variables for further calculations
    borefield._reset_for_sizing(borefield.N_1, borefield.N_2)
    # reset printing
    borefield.printing: bool = printing_backup
    # save result list
    borefield.combo = combo
    # return results list
    return combo


def size_complete_field_fast(self, H_max: float, l_1: float, l_2: float, B_min: float = 3.0, B_max: float = 9.0,
                             L2_sizing: bool = True, use_constant_Rb: bool = False) -> list:
    """
    Function to size the minimal number of borefield by borefield length and width on a fast and not robust way.
    There are possible solution that can not be found.
    :param H_max: maximal borehole depth [m]
    :param l_1: maximal width of borehole field [m]
    :param l_2: maximal length of borehole field [m]
    :param B_min: minimal borehole spacing [m]
    :param B_max: maximal borehole spacing [m]
    :param L2_sizing: boolean to check if level two or level three sizing method should be used
    :param use_constant_Rb: boolean to check if a constant borehole resistance should be used
    :return: list of possible combinations (each combination is a tuple where the first two elements are the
    number of boreholes in each direction, the third element the borehole spacing and the last element
    the depth of the borefield). An Empty list is returned if no results is found
    """
    # check if length > width
    l2_bigger_then_l1: bool = l_2 > l_1
    # change length and width if length > width
    (l_1, l_2) = (l_2, l_1) if l2_bigger_then_l1 else (l_1, l_2)
    # set start maximal number of boreholes
    n_n_max_start: int = 21 * 21
    # set maximal number of boreholes
    n_n_max: int = n_n_max_start
    # list of possible combinations
    combo: list = []
    # deactivate printing
    printing_backup = self.printing
    self.printing: bool = False
    # start loop over borehole spacing
    for B in np.arange(B_max, B_min * 0.99999, -0.5):
        # calculate maximal number of boreholes in length and width direction
        N1_max = min(int(l_1 / B), 20)
        N2_max = min(int(l_2 / B), 20)
        # reset variables for sizing
        self._reset_for_sizing(N1_max, N2_max)
        # set borehole spacing
        self.B = B
        # save start configuration to product old
        total_number_boreholes_old = self.N_1 * self.N_2
        # try to determine depth and break loop if unsuccessful
        try:
            # size current borefield configuration
            depth = self.size(H_max, L2_sizing=L2_sizing, L3_sizing=not L2_sizing, use_constant_Rb=use_constant_Rb)
            # determine required number of boreholes
            number_boreholes = int(depth * total_number_boreholes_old / H_max) + 1
            # determine number of boreholes in length and width direction which accomplish the total number of
            # boreholes
            res = self._calc_number_boreholes(number_boreholes, N1_max, N2_max)
            # reset variables for sizing
            self._reset_for_sizing(res[0][0], res[0][1])
            # determine new total number of boreholes
            total_number_boreholes_new = self.N_1 * self.N_2
            # start counter
            counter = 0
            # start while loop to size borefield
            while total_number_boreholes_old != total_number_boreholes_new:
                # determine gradient to calculate new total borehole number if counter > 4 with a gradient of 0.51
                # else 1
                gradient = int(0.51 * (total_number_boreholes_new - total_number_boreholes_old)) if counter > 4 \
                    else int(total_number_boreholes_new - total_number_boreholes_old)
                # determine new total borehole number
                total_number_boreholes_new = total_number_boreholes_old + np.sign(gradient) * min(abs(gradient), 1)
                # determine depth for the new configuration
                depth = self.size(H_max, L2_sizing, use_constant_Rb=use_constant_Rb)
                # determine new total number of boreholes
                number_boreholes = int(depth * total_number_boreholes_new / H_max) + 1
                # determine number of boreholes in length and width directions
                res = self._calc_number_boreholes(number_boreholes, N1_max, N2_max)
                # reset borefield variables for sizing
                self._reset_for_sizing(res[0][0], res[0][1])
                # set old total number of boreholes
                total_number_boreholes_old = self.N_1 * self.N_2
                # count counter
                counter += 1
                # break loop if counter is higher than 20 and the depth is below the maximal depth
                if counter > 20 and depth <= H_max:
                    break
            # save configuration if new total number of boreholes is smaller than the maximal number so far
            if total_number_boreholes_new < n_n_max:
                # save new maximal number
                n_n_max = total_number_boreholes_new
                # if more than 1 result is found calculate the depth and append the solution if it fits maximal
                # depth
                if len(res) > 1:
                    # reset list
                    combo: list = []
                    # reset boolean for first element
                    first: bool = True
                    # start loop over possible solutions
                    for i in res:
                        # if first element just append results
                        if first:
                            combo.append([i[0], i[1], B, self.H])
                            first = False
                            continue
                        # if not first element reset variables and determine new depth and then append if it fits
                        # the maximal depth
                        self._reset_for_sizing(i[0], i[1])
                        self.size(H_max, L2_sizing, use_constant_Rb=use_constant_Rb)
                        if self.H < H_max:
                            combo.append([i[0], i[1], B, self.H])
                else:
                    # just create the list if just one solution is found
                    combo = [[res[0][0], res[0][1], B, self.H]]
            # append solutions if the same total number of boreholes is found as the current maximal number
            elif total_number_boreholes_new == n_n_max:
                # if more than 1 result is found calculate the depth and append the solution if it fits maximal
                # depth
                if len(res) > 1:
                    first: bool = True
                    for i in res:
                        # if first element just append results
                        if first:
                            combo.append([i[0], i[1], B, self.H])
                            first = False
                            continue
                        # if not first element reset variables and determine new depth and then append if it fits
                        # the maximal depth
                        self._reset_for_sizing(i[0], i[1])
                        self.size(H_max, L2_sizing, use_constant_Rb=use_constant_Rb)
                        if self.H < H_max:
                            combo.append([i[0], i[1], B, self.H])
                else:
                    # just append list if just one solution is found
                    combo += [[res[0][0], res[0][1], B, self.H]]

        except ValueError:
            # break if no result can be found, because depth is too deep for precalculated data
            break
    # if no solution is found return an empty list
    if n_n_max == n_n_max_start:
        return []
    # change N_1 and N_2 if length > width
    combo = [[i[1], i[0], i[2], i[3]] for i in combo] if l2_bigger_then_l1 else combo
    # set number of boreholes in length and width, borehole spacing and depth
    self.N_1 = combo[0][1]
    self.N_2 = combo[0][0]
    self.B = combo[0][2]
    self.H = combo[0][3]
    # reset variables for further calculations
    self._reset_for_sizing(self.N_1, self.N_2)
    # activate printing
    self.printing: bool = printing_backup
    # save result list
    self.combo = combo
    # return results list
    return combo


def fun_new(n_min: int, L_max: int, B_max: int) -> list[tuple[int, int]]:
    #min_val = 0
    B_max = min(n_min, B_max)
    L_max = min(n_min, L_max)
    """
    b_max = max(B_max, L_max)
    #b_min = min(B_max, L_max)
    for b in range(1, b_max + 1):
        val = int(n_min/b) + (n_min % b>0)
        if val <= b_max:
            min_val = val * b
            break
    return [(b, l) for b in range(1, B_max + 1) for l in range(1, L_max+1) if l * b == min_val]

    """
    li = [(l, b, l * b) for b in range(1, B_max+1) for l in range(int(n_min/b) + (n_min % b>0), L_max+1) if n_min <= l * b]
    if not li:
        return []
    min_val = min(val for _, _, val in li)
    return [(b, l) for b, l, val in li if val == min_val]


def _calc_number_boreholes(n_min: int, N1_max: int, N2_max: int) -> list:
    """
    calculation for number of boreholes which is higher than n but minimal total number
    :param n_min: minimal number of boreholes
    :param N1_max: maximal width of rectangular field (#)
    :param N2_max: maximal length of rectangular field (#)
    :return: list of possible solutions
    """
    # set default result
    res = []
    N1_max = min(n_min, N1_max)
    N2_max = min(n_min, N2_max)
    # set maximal number
    max_val = N1_max * N2_max + 1
    # loop over maximal number in width and length
    for l in range(1, N1_max + 1):
        for b in range(int(n_min/l) + (n_min % l>0), N2_max + 1):
            # determine current number
            current_number: int = l * b
            # save number of boreholes  and maximal value if is lower than current maximal value and higher than
            # minimal value
            if n_min <= current_number < max_val:
                res = [(l, b)]
                max_val = current_number
            # also append combination if current number is equal to current maximal value
            elif current_number == max_val:
                res.append((l, b))
    # return list of possible solutions
    return res


if __name__ == "__main__":  # pragma: no cover
    from time import process_time_ns

    res_old = []
    dt1 = process_time_ns()
    for i in range(1, 40):
        for j in range(1, 50):
            for n_min_i in range(1, 40):
                res_old.append((_calc_number_boreholes(n_min_i, i, j), (n_min_i, i, j)))

    dt2 = process_time_ns()
    print(f"old {(dt2-dt1)/1000_000_000} sec")
    res_new = []
    dt1 = process_time_ns()
    for i in range(1, 40):
        for j in range(1, 50):
            for n_min_i in range(1,40):
                res_new.append((fun_new(n_min_i, i, j), (n_min_i, i, j)))

    dt2 = process_time_ns()
    print(f"new {(dt2-dt1)/1000_000_000} sec")

    for val_new, val_old in zip(res_new, res_old):
        for v1 in val_new[0]:
            if not v1 in val_old[0]:
                # print(v1, val_old)
                v1 = (v1[1], v1[0])
                if not v1 in val_old[0]:
                    print(v1, val_old)
            assert v1 in val_old[0]
        for v1 in val_old[0]:
            if not v1 in val_new[0]:
                # print(v1, val_new)
                v1 = (v1[1], v1[0])
                if not v1 in val_new[0]:
                    print(v1, val_new)
            assert v1 in val_new[0]

