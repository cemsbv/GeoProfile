import logging
from typing import Any, Dict, List, Literal, Optional, Union

import numpy as np
from numpy.typing import NDArray
from plotly import graph_objects as go
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots
from python_tsp.exact import solve_tsp_dynamic_programming
from scipy import spatial
from shapely.geometry import LineString, Point
from skspatial.objects import Line
from tqdm import tqdm

from geoprofile.column import Column

# optional imports
try:
    import contextily as ctx
    import geopandas as gpd
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import Axes
except ImportError:
    ctx = None
    gpd = None
    plt = None
    Axes = None


class Section:
    def __init__(
        self,
        data_list: List[Column],
        profile_line: LineString,
        buffer: float = 10,
        sorting_algorithm: Literal[
            "tsp", "nearest_neighbor", "custom"
        ] = "nearest_neighbor",
        reproject: bool = True,
    ) -> None:
        """
        Class that filters, sorts and plot columns based on a profile line.

        Parameters
        ----------
        data_list: list
            List with Column classes.
        profile_line: LineString
            Profile line of the cross section.
            It is linestring a list of (x, y) coordinates.
            Example: LineString([(x1, y1), (x2, y2), ...])
        buffer: float, optional
            Default is 10
            Buffer distance use to include columns in the profile [m]
        sorting_algorithm: Literal["tsp", "nearest_neighbor", "custom"], optional
            Default is nearest_neighbor.
            Define the sorting algorithm use to sort the data points.
            Can be one of the following:
                - tsp (traveling salesman problem)
                - nearest_neighbor
                - custom
        reproject: bool, optional
            Default is True
            Reproject points of the column onto the profile line.
        """

        if buffer <= 0:
            raise ValueError("Buffer distance cannot be less than zero")

        if sorting_algorithm not in ["tsp", "custom", "nearest_neighbor"]:
            raise ValueError("Sorting option not available")

        self._data_list = data_list
        self._profile_line = profile_line
        self._buffer = buffer
        self._sorting_algorithm = sorting_algorithm
        self._reproject = reproject

        # validate data
        if len(data_list) != len(set(map(lambda x: x.name, data_list))):
            logging.warning("No unique names in columns")

        if len(data_list) != len(set(map(lambda x: frozenset((x.x, x.y)), data_list))):
            logging.warning("No unique coordinates in columns")

    @property
    def reproject(self) -> bool:
        """reproject points of the column onto the profile line."""
        return self._reproject

    @property
    def profile_line(self) -> LineString:
        """profile line of the scoss section."""
        return self._profile_line

    @property
    def data_list_all(self) -> List[Column]:
        """all columns provided by initializing the class"""
        return self._data_list

    @property
    def buffer(self) -> float:
        """buffer distance use to include columns in the profile [m]"""
        return self._buffer

    @property
    def sorting_algorithm(self) -> str:
        """sorting algorithm used to sort columns to profile line"""
        return self._sorting_algorithm

    @property
    def profile_polygon(self) -> LineString:
        """polygon create based on the profile line and the buffer argument"""
        return self.profile_line.buffer(self.buffer, cap_style=2, join_style=1)

    @property
    def coordinates_all(self) -> NDArray[np.floating]:
        """list of coordinates of the all the column locations"""
        return np.array(
            list(
                map(
                    lambda item: (item.x, item.y),
                    self.data_list_all,
                )
            )
        )

    @property
    def coordinates_include(self) -> NDArray[np.floating]:
        """list of coordinates of the selected column locations"""
        return np.array(
            list(
                map(
                    lambda item: (item.x, item.y),
                    self.data_list_include,
                )
            )
        )

    @property
    def data_list_include(self) -> List[Column]:
        """selected columns based on profile polygon"""

        data_list_include = []
        for item in self.data_list_all:
            if Point(item.x, item.y).covered_by(self.profile_polygon):
                data_list_include.append(item)

        if len(data_list_include) < 1:
            raise ValueError(
                "No data points are selected. Change the profile line or increase the buffer distance."
            )

        return data_list_include

    @property
    def distance_matrix_include(self) -> NDArray[np.floating]:
        """Compute the distance matrix. Returns the matrix of all pair-wise distances [m]."""
        distance_matrix = spatial.distance_matrix(
            self.coordinates_include,
            self.coordinates_include,
        )
        return distance_matrix

    @property
    def distance_matrix_include_reprojection(self) -> NDArray[np.floating]:
        """Compute the distance matrix. Returns the matrix of all pair-wise distances [m]."""

        # make sure the data list order is consistent
        coordinates = [
            self.coordinates_include_reprojection[i]
            for i in range(len(self.data_list_include))
        ]

        distance_matrix = spatial.distance_matrix(
            np.array(coordinates),
            np.array(coordinates),
        )
        return distance_matrix

    @property
    def start_node(self) -> int:
        """Closed column point on the start of the profile line"""
        return spatial.distance_matrix(
            self.coordinates_include,
            list(zip(*self.profile_line.xy)),
        ).argmin(axis=0)[0]

    @property
    def end_node(self) -> int:
        """Closed column point on the end of the profile line"""
        return spatial.distance_matrix(
            self.coordinates_include,
            list(zip(*self.profile_line.xy)),
        ).argmin(axis=0)[-1]

    @property
    def coordinates_include_reprojection(self) -> Dict[Union[int, str], List[float]]:
        """list of coordinates of the selected column locations reprojected on the profile line"""

        nodes = list(zip(*self.profile_line.xy))
        projected_point: Dict[Union[int, str], List[float]] = {}

        for sigment in range(len(nodes) - 1):
            for i, item in enumerate(self.coordinates_include):
                if Point(item[0], item[1]).covered_by(
                    LineString((nodes[sigment], nodes[sigment + 1])).buffer(
                        self.buffer, cap_style=2, join_style=1
                    )
                ):
                    line = Line.from_points(
                        point_a=nodes[sigment], point_b=nodes[sigment + 1]
                    )
                    point = line.project_point((item[0], item[1]))
                    projected_point[i] = [point[0], point[1]]
        return projected_point

    @property
    def sorting(self) -> tuple:
        """
        Based on the soring algorithm the columns are sorted.

        Returns
        -------
        permutation
            A permutation of nodes from 0 to n that produces the least total
            distance

        distance
            The total distance the optimal permutation produces
        """

        if self.sorting_algorithm == "tsp":
            # place start column first
            start_node = (
                spatial.distance_matrix(
                    self.coordinates_all,
                    list(zip(*self.profile_line.xy)),
                )
                .argmin(axis=0)[0]
                .copy()
            )

            self._data_list.insert(0, self._data_list[start_node])
            self._data_list.pop(start_node)

            if self.reproject:
                distance_matrix = self.distance_matrix_include_reprojection
            else:
                distance_matrix = self.distance_matrix_include

            # change the cost function such that every arc to
            # the depot has cost 0. To create an open tsp
            distance_matrix[:, self.start_node] = 0

            return solve_tsp_dynamic_programming(distance_matrix, maxsize=128)

        elif self.sorting_algorithm == "nearest_neighbor":
            if self.reproject:
                distance_matrix = self.distance_matrix_include_reprojection
            else:
                distance_matrix = self.distance_matrix_include

            # replace all self correlated distances to nan
            distance_matrix[np.diag_indices(len(self.data_list_include))] = np.nan

            permutation = [self.start_node]
            while len(permutation) != len(self.coordinates_include):
                # add next column to permutation list
                permutation.append(
                    np.nanargmin(distance_matrix, axis=0)[permutation[-1]]
                )

                # set inf to used columns in distance_matrix
                distance_matrix[:, permutation[-2]] = np.inf
                distance_matrix[permutation[-2], :] = np.inf

            return (
                permutation,
                LineString(
                    [self.coordinates_include[i].tolist() for i in permutation]
                ).length,
            )

        elif self.sorting_algorithm == "custom":
            if self.reproject:
                return (
                    list(range(0, len(self.data_list_include))),
                    LineString(self.coordinates_include_reprojection).length,
                )
            else:
                return (
                    list(range(0, len(self.data_list_include))),
                    LineString(self.coordinates_include).length,
                )
        else:
            raise ValueError

    def plot_map(
        self,
        axis: Optional[Axes] = None,
        add_basemap: bool = False,
        add_tags: bool = True,
        tag_type: Literal["name", "index"] = "name",
        show_all: bool = False,
    ) -> Axes:
        """
        Create a map that contain the following:
            - location of the columns (gray point)
            - location of the selected columns (black point)
            - profile line (gray line)
            - profile polygon (light gray area)
            - re-projection (black line)

        Parameters
        ----------
        axis : plt.Axes, optional
            plt.Axes used to create the map
        add_basemap : bool, optional
            default is False
            Flag that includes basemap in figure.
        add_tags : bool, optional
            default is True
            Show the CPT names or indices as tags on the map.
        tag_type : str, optional
            default is "name"
            Type of tag to show on the map. Can be either "name" or "index".
        show_all : bool, optional
            default is False
            Show all columns on the map, not just the selected ones.

        Returns
        -------
        plt.Axes
        """
        if gpd is None or plt is None:
            raise ImportError("No module named 'geopandas' or matplotlib")

        if axis is None:
            # plot all column locations
            axis = gpd.GeoDataFrame(
                geometry=gpd.points_from_xy(*zip(*self.coordinates_all)),
                crs="EPSG:28992",
            ).plot(color="grey")
        else:
            # plot all column locations
            gpd.GeoDataFrame(
                geometry=gpd.points_from_xy(*zip(*self.coordinates_all)),
                crs="EPSG:28992",
            ).plot(ax=axis, color="grey")

        # add the use defined profile line
        gpd.GeoSeries(
            [self.profile_line],
            crs="EPSG:28992",
        ).plot(ax=axis, color="grey")

        # add the use defined profile line
        gpd.GeoSeries(
            [self.profile_polygon],
            crs="EPSG:28992",
        ).plot(ax=axis, color="grey", alpha=0.3)

        # plot all column locations that are included
        gpd.GeoDataFrame(
            geometry=gpd.points_from_xy(*zip(*self.coordinates_include)),
            crs="EPSG:28992",
        ).plot(ax=axis, color="black")

        # add the use sorting defined profile line
        x = []
        y = []
        for node in self.sorting[0]:
            x.append(self.data_list_include[node].x)
            y.append(self.data_list_include[node].y)
        axis.plot(x, y, "-")

        # add re-projection of point to line
        if self.reproject:
            for key, value in self.coordinates_include_reprojection.items():
                plt.annotate(
                    "",
                    xy=self.coordinates_include[key],
                    xycoords="data",
                    xytext=value,
                    textcoords="data",
                    arrowprops=dict(arrowstyle="-", connectionstyle="arc3,rad=0."),
                )

        # add labels (column names) to map
        if add_tags:
            if tag_type not in ["name", "index"]:
                raise ValueError("tag_type must be either 'name' or 'index'")

            for i, item in enumerate(
                self.data_list_include if not show_all else self.data_list_all
            ):
                axis.annotate(
                    str(i) if tag_type == "index" else item.name,
                    xy=(item.x, item.y),
                    xytext=(3, 3),
                    textcoords="offset points",
                )

        # add base map
        if add_basemap:
            if ctx is None:
                raise ImportError("No module named 'contextily'")
            ctx.add_basemap(
                axis, crs="EPSG:28992", source=ctx.providers.OpenStreetMap.Mapnik
            )
        axis.ticklabel_format(useOffset=False, style="plain")
        plt.tight_layout()
        return axis

    def plot(
        self,
        figure: Optional[Figure] = None,
        x0: float = 0.0,
        groundwater_level: bool = False,
        surface_level: bool = False,
        **kwargs: Any,
    ) -> Figure:
        """
        Create profile based on the column's location, sorting algorithm and profile line.

        Parameters
        ----------
        figure: Figure, optional
            A plotly Figure to add the profile to.
        x0: float, optional
            Default is 0.0
            Start of the profile line.
        groundwater_level: bool, optional
            Default is False
            Flag that indicated if groundwater level is added to the profile
        surface_level: bool, optional
            Default is False
            Flag that indicated if groundwater level is added to the profile
        kwargs: Any
            kwargs past to the column plot function.

        Returns
        -------
        plotly.graph_objs.Figure
        """
        if kwargs is None:
            kwargs = {}

        # get sorting list and profile distance
        permutation, distance = self.sorting

        # get the coordinates of the columns
        if self.reproject:
            coordinates_dict = self.coordinates_include_reprojection
            coordinates_dict["start_line"] = [
                self.profile_line.xy[0][0],
                self.profile_line.xy[1][0],
            ]
            coordinates_dict["end_line"] = [
                self.profile_line.xy[0][-1],
                self.profile_line.xy[1][-1],
            ]
            distance = self.profile_line.length

        else:
            coordinates_dict = dict(
                zip(
                    permutation,
                    [self.coordinates_include[i].tolist() for i in permutation],
                )
            )
            coordinates_dict["start_line"] = [
                coordinates_dict[permutation[0]][0],
                coordinates_dict[permutation[0]][1],
            ]
            coordinates_dict["end_line"] = [
                coordinates_dict[permutation[-1]][0],
                coordinates_dict[permutation[-1]][1],
            ]

        if figure is None:
            # initialize plot
            figure = make_subplots(
                rows=1,
                cols=1,
                y_title="Depth [m REF]",
                shared_yaxes=True,
                horizontal_spacing=0.01,
                column_widths=[distance],
            )

        # duplicate start and endpoint
        permutation.insert(0, "start_line")
        permutation.append("end_line")

        # placeholders
        groundwater_level_list = []
        surface_level_list = []
        center_list = []

        # loop over permutation
        for i in tqdm(range(1, len(permutation) - 1), desc="Add column to profile"):
            # right side
            d_right = (
                LineString(
                    (
                        (
                            coordinates_dict[permutation[i]][0],
                            coordinates_dict[permutation[i]][1],
                        ),
                        (
                            coordinates_dict[permutation[i + 1]][0],
                            coordinates_dict[permutation[i + 1]][1],
                        ),
                    )
                ).length
                / 2
            )

            # left side
            d_left = (
                LineString(
                    (
                        (
                            coordinates_dict[permutation[i]][0],
                            coordinates_dict[permutation[i]][1],
                        ),
                        (
                            coordinates_dict[permutation[i - 1]][0],
                            coordinates_dict[permutation[i - 1]][1],
                        ),
                    )
                ).length
                / 2
            )

            # add columns to profile
            self.data_list_include[permutation[i]].plot(
                figure,
                **kwargs,
                x0=x0,
                d_left=d_left,
                d_right=d_right,
                profile=True,
            )

            # fill list
            center_list.append(x0 + d_left)
            groundwater_level_list.append(
                self.data_list_include[permutation[i]].groundwater_level
            )
            surface_level_list.append(self.data_list_include[permutation[i]].z)

            # set the starting point of the next column
            x0 += d_left + d_right

        # Add dashed blue line representing phreatic level
        if groundwater_level:
            figure.add_trace(
                go.Scatter(
                    name="Groundwater level [m REF]",
                    x=center_list,
                    y=groundwater_level_list,
                    line=dict(color="Blue", dash="dash", width=1),
                    showlegend=True,
                )
            )

        # Add dashed brown line representing ground level
        if surface_level:
            figure.add_trace(
                go.Scatter(
                    name="Surface level [m REF]",
                    x=center_list,
                    y=surface_level_list,
                    line=dict(color="Brown", dash="dash", width=1),
                    showlegend=True,
                )
            )
        return figure
