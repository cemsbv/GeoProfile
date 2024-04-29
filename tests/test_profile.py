import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objs as go
from shapely.geometry import LineString

from geoprofile import Column, Section


def test_sorting(classify_dict: dict) -> None:
    columns = [
        Column(classify_dict, 0, 0),
        Column(classify_dict, 10, 10),
        Column(classify_dict, 10, 0),
    ]

    profile = Section(
        columns,
        profile_line=LineString(((0, 0), (10, 0), (10, 10))),
        sorting_algorithm="custom",
        reproject=False,
    )
    assert profile.sorting == ([0, 1, 2], (np.sqrt(10**2 + 10**2)) + 10)

    profile = Section(
        columns,
        profile_line=LineString(((0, 0), (10, 0), (10, 10))),
        sorting_algorithm="tsp",
        reproject=False,
    )
    assert profile.sorting == ([0, 2, 1], (10 + 10))

    profile = Section(
        columns,
        profile_line=LineString(((0, 0), (10, 0), (10, 10))),
        sorting_algorithm="nearest_neighbor",
        reproject=False,
    )
    assert profile.sorting == ([0, 2, 1], (10 + 10))


def test_selecting(classify_dict: dict) -> None:
    columns = [
        Column(classify_dict, 0, 0),
        Column(classify_dict, 10, 10),
        Column(classify_dict, 10, 0),
    ]

    profile = Section(columns, profile_line=LineString(((0, 0), (10, 0))), buffer=1)
    assert len(profile.data_list_include) == 2

    profile = Section(columns, profile_line=LineString(((0, 0), (10, 0))), buffer=12)
    assert len(profile.data_list_include) == 3


def test_reprojecting(classify_dict: dict) -> None:
    columns = [
        Column(classify_dict, 3, 1),
        Column(classify_dict, 9, 9),
        Column(classify_dict, 10, -1),
    ]

    profile = Section(
        columns, profile_line=LineString(((0, 0), (10, 0), (10, 10))), buffer=1
    )
    assert profile.coordinates_include_reprojection == {
        0: [3.0, 0.0],
        2: [10.0, 0.0],
        1: [10.0, 9.0],
    }


def test_plot(classify_dict: dict) -> None:
    columns = [
        Column(classify_dict, 3, 1),
        Column(classify_dict, 9, 9),
        Column(classify_dict, 10, -1),
    ]

    profile = Section(
        columns, profile_line=LineString(((0, 0), (10, 0), (10, 10))), buffer=1
    )
    assert isinstance(profile.plot_map(), plt.Axes)
    assert isinstance(profile.plot(), go.Figure)
