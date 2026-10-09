import os

import numpy as np
import pandas as pd
from matplotlib.colors import to_rgba_array

from points_decorator import points
from plot_checks import (
    section, scatter_collections, titles, all_axes, norm, is_valid_png, as_float_array,
)

N_POINTS = 1000


class TestProblem1:
    @points(0.5, "Problem 1, Part 1: Did you create a DataFrame `data` with columns `x` and `y` holding 1000 random float values?")
    def test_problem_1_part_1(self, problem1):
        section_data, namespace = problem1
        variables = section(section_data, "Part 1")["variables"]

        data = variables["data"]
        assert isinstance(data, pd.DataFrame)
        assert len(data) == N_POINTS
        for col in ("x", "y"):
            assert col in data.columns
            values = as_float_array(data[col])
            # Random values should not all be the same
            assert len(np.unique(values)) > 1

    @points(0.5, "Problem 1, Part 2: Did you create a variable `colors` holding 1000 random float values?")
    def test_problem_1_part_2(self, problem1):
        section_data, namespace = problem1
        variables = section(section_data, "Part 2")["variables"]

        colors = variables["colors"]
        assert len(colors) == N_POINTS
        values = as_float_array(colors)
        assert len(np.unique(values)) > 1

    @points(0.5, "Problem 1, Part 3: Your figure should be a scatter plot of the 1000 points coloured with the random `colors` values.")
    def test_problem_1_part_3_scatter(self, problem1):
        section_data, namespace = problem1
        figures = section(section_data, "Part 3")["figures"]
        assert figures, "No figure was created in Part 3"

        scatters = [coll for _, coll in scatter_collections(figures)
                    if len(coll.get_offsets()) == N_POINTS]
        assert scatters, "No scatter plot with 1000 points found"

        coll = scatters[0]
        mapped = coll.get_array()
        if mapped is not None and len(mapped) == N_POINTS:
            # Colours given as values + colormap
            assert len(np.unique(np.asarray(mapped))) > 1
        else:
            # Colours given directly
            facecolors = to_rgba_array(coll.get_facecolor())
            assert len(np.unique(facecolors, axis=0)) > 1

    @points(0.5, "Problem 1, Part 3: Did you add a title to your plot (stored in the variable `title`)?")
    def test_problem_1_part_3_title(self, problem1):
        section_data, namespace = problem1
        part = section(section_data, "Part 3")
        title = part["variables"]["title"]
        assert isinstance(title, str) and title.strip()
        assert norm(title) in [norm(t) for t in titles(part["figures"])]

    @points(0.5, "Problem 1, Part 3: Did you add x- and y-labels to your plot (stored in the variables `xlabel` and `ylabel`)?")
    def test_problem_1_part_3_labels(self, problem1):
        section_data, namespace = problem1
        part = section(section_data, "Part 3")
        xlabel = part["variables"]["xlabel"]
        ylabel = part["variables"]["ylabel"]
        assert isinstance(xlabel, str) and xlabel.strip()
        assert isinstance(ylabel, str) and ylabel.strip()

        axes = all_axes(part["figures"])
        assert norm(xlabel) in [norm(ax.get_xlabel()) for ax in axes]
        assert norm(ylabel) in [norm(ax.get_ylabel()) for ax in axes]

    @points(0.5, "Problem 1, Part 3: Did you save your plot as a PNG file `my_first_plot.png` using the variable `outputfp`?")
    def test_problem_1_part_3_saved(self, problem1):
        section_data, namespace = problem1
        outputfp = section(section_data, "Part 3")["variables"]["outputfp"]
        assert os.path.basename(str(outputfp)) == "my_first_plot.png"
        assert is_valid_png(outputfp)
