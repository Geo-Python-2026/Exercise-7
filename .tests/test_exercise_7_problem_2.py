import os
import pathlib

import numpy as np
import pandas as pd
import pytest
from matplotlib.colors import to_rgba

from points_decorator import points
from plot_checks import section, lines, titles, all_axes, norm, is_valid_png

DATA_FP = pathlib.Path(__file__).absolute().parent.parent / "data" / "helsinki-vantaa.csv"
START, END = "1988-01-01", "2018-12-31"


@pytest.fixture(scope="module")
def expected():
    """Reference answer computed from the input data."""
    data = pd.read_csv(DATA_FP, parse_dates=["DATE"], index_col="DATE").sort_index()
    return {"n_rows": len(data), "selection": data.loc[START:END]}


def _temperature_line(figures, expected_temps):
    """Return the plotted line that contains the TEMP_C values of the selection, if any."""
    target = np.sort(expected_temps.to_numpy(dtype=float))
    for ax, line in lines(figures):
        y = np.asarray(line.get_ydata(), dtype=float)
        if len(y) == len(target) and np.allclose(np.sort(y), target, equal_nan=True):
            return line
    return None


class TestProblem2:
    @points(0.5, "Problem 2, Part 1: Variable `data` does not exist or has incorrect length!")
    def test_problem_2_part_1_len(self, problem2, expected):
        section_data, namespace = problem2
        variables = section(section_data, "Part 1")["variables"]

        assert isinstance(variables["data"], pd.DataFrame)
        assert len(variables["data"]) == expected["n_rows"]

    @points(0.5, "Problem 2, Part 1: Did you set the date as index of the dataframe?")
    def test_problem_2_part_1_index(self, problem2):
        section_data, namespace = problem2
        variables = section(section_data, "Part 1")["variables"]

        assert isinstance(variables["data"].index, pd.DatetimeIndex)

    @points(1, "Problem 2, Part 2: The dataframe `selection` should start in January 1988.")
    def test_problem_2_part_2_start(self, problem2, expected):
        section_data, namespace = problem2
        selection = section(section_data, "Part 2")["variables"]["selection"]

        assert isinstance(selection.index, pd.DatetimeIndex)
        assert selection.index.min() == expected["selection"].index.min()
        assert np.isclose(selection.loc[selection.index.min(), "TEMP_C"],
                          expected["selection"]["TEMP_C"].iloc[0])

    @points(1, "Problem 2, Part 2: The dataframe `selection` should end in December 2018 and cover all months in between.")
    def test_problem_2_part_2_end(self, problem2, expected):
        section_data, namespace = problem2
        selection = section(section_data, "Part 2")["variables"]["selection"]

        assert selection.index.max() == expected["selection"].index.max()
        assert len(selection) == len(expected["selection"])

    @points(1, "Problem 2, Part 3: Your figure should be a line plot of the monthly temperatures (`TEMP_C`) for 1988-2018.")
    def test_problem_2_part_3_line(self, problem2, expected):
        section_data, namespace = problem2
        figures = section(section_data, "Part 3")["figures"]
        assert figures, "No figure was created in Part 3"

        assert _temperature_line(figures, expected["selection"]["TEMP_C"]) is not None

    @points(1, "Problem 2, Part 3: The line should be solid and black with round markers.")
    def test_problem_2_part_3_style(self, problem2, expected):
        section_data, namespace = problem2
        figures = section(section_data, "Part 3")["figures"]

        line = _temperature_line(figures, expected["selection"]["TEMP_C"])
        assert line is not None
        assert line.get_linestyle() == "-"
        assert np.allclose(to_rgba(line.get_color())[:3], (0, 0, 0))
        assert line.get_marker() in ("o", ".")

    @points(1, "Problem 2, Part 3: Did you add the title 'Helsinki-Vantaa Airport' and the axis labels 'Time' and 'Temperature (Celsius)' (stored in `title`, `xlabel` and `ylabel`)?")
    def test_problem_2_part_3_labels(self, problem2):
        section_data, namespace = problem2
        part = section(section_data, "Part 3")
        variables, figures = part["variables"], part["figures"]

        assert norm(variables["title"]) == norm("Helsinki-Vantaa Airport")
        assert norm(variables["xlabel"]) == norm("Time")
        assert norm(variables["ylabel"]) == norm("Temperature (Celsius)")

        axes = all_axes(figures)
        assert norm(variables["title"]) in [norm(t) for t in titles(figures)]
        assert norm(variables["xlabel"]) in [norm(ax.get_xlabel()) for ax in axes]
        assert norm(variables["ylabel"]) in [norm(ax.get_ylabel()) for ax in axes]

    @points(1, "Problem 2, Part 3: Did you save your plot as a PNG file `temp_line_plot.png` using the variable `outputfp`?")
    def test_problem_2_part_3_saved(self, problem2):
        section_data, namespace = problem2
        outputfp = section(section_data, "Part 3")["variables"]["outputfp"]

        assert os.path.basename(str(outputfp)) == "temp_line_plot.png"
        assert is_valid_png(outputfp)
