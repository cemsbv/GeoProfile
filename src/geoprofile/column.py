import copy
import logging
from typing import Dict, List, Optional, Union

import numpy as np
from PIL import ImageColor
from plotly import graph_objects as go
from plotly.graph_objects import Figure
from plotly.subplots import make_subplots

from geoprofile.constant import CODING_SOIL_TYPES

# optional import
try:
    from pygef.bore import BoreData
    from pygef.cpt import CptData
except ImportError:
    CptData = None
    BoreData = None

DEFAULT_COLUMN_WIDTH = 1


class Column:
    def __init__(
        self,
        classify: Dict[str, List[Union[float, str]]],
        x: float,
        y: float,
        name: str = "N/A",
        z: Optional[float] = None,
        groundwater_level: Optional[float] = None,
        data: Optional[Dict[str, List[float]]] = None,
    ) -> None:
        """
        Holds the data related to a column in the profile.

        Parameters
        ----------
        classify: dict
            Dictionary that holds the classification data. Must
            contain the following keys:

                - depth
                    Top of the layers [m REF]
                - thickness
                    Thickness of the layer [m]
                - geotechnicalSoilName
                    Soil code of the layer related to the NEN-EN-ISO 14688-1:2019+NEN 8990:2020 Tabel NA.17

        Other Parameters
        -----------------
        x: float
            x coordinate of the column. Must be in a Cartesian coordinate system
        y: float
            x coordinate of the column. Must be in a Cartesian coordinate system
        name: str, optional
            default is N/A
            Name of the location.
        z: float, optional
            Default is None
            surface level of the column [m REF].
        groundwater_level: float, optional
            Default is None
            groundwater level of the column [m REF].
        data: dict
            Default is None
            Other data that can be added to the plot. If not None than dictionary
            must contain the following key:

                - depth
                    Top of the layers [m REF]
        """
        # validate
        if any(
            [
                key not in ["depth", "thickness", "geotechnicalSoilName"]
                for key in classify.keys()
            ]
        ):
            raise ValueError("Key missing in classify dictionary.")

        if any(
            [len(classify["depth"]) != len(classify[key]) for key in classify.keys()]
        ):
            raise ValueError(
                "Value arrays of classify dictionary do not have the same dimensions"
            )

        for key in classify["geotechnicalSoilName"]:
            if key not in CODING_SOIL_TYPES.keys():
                raise ValueError(
                    f"geotechnicalSoilName `{key}` not in CODING_SOIL_TYPES [NEN-EN-ISO 14688-1:2019+NEN 8990:2020 "
                    "Tabel NA.17] dictionary."
                )

        if data is not None:
            if "depth" not in classify.keys():
                raise ValueError("Key missing in data dictionary.")

        if any(
            [len(classify["depth"]) != len(classify[key]) for key in classify.keys()]
        ):
            raise ValueError(
                "Value arrays of data dictionary do not have the same dimensions"
            )

        self._classify = classify
        self._x = x
        self._y = y
        self._z = z
        self._groundwater_level = groundwater_level
        self._name = name

        # set optional attributes
        if data is None:
            data = {}
        self._data = data

    @classmethod
    def from_cpt(cls, response: dict, gef: CptData) -> "Column":
        """
        Use the cptcore response to translate the NEN6740 Table 2B to the NEN-EN-ISO 14688-1:2019+NEN 8990:2020 Tabel NA.17

        Parameters
        ----------
        response: dict
            response of the CPT Core classify API call
        gef: pygef.cpt.CptData
            CPT object created by pygef.

        Returns
        -------
        Column
        """

        classify = {
            "depth": gef.delivered_vertical_position_offset
            - np.array(response.get("upperBoundary")),
            "thickness": (
                np.array(response.get("lowerBoundary"))
                - np.array(response.get("upperBoundary"))
            ).tolist(),
            "geotechnicalSoilName": [
                name.split(";")[0].replace("*", "")
                for name in response.get("geotechnicalSoilName", [])
            ],
        }

        if "depth" in gef.columns:
            data = gef.data.drop("depth").rename({"depthOffset": "depth"}).to_dict()
        else:
            data = gef.data.rename({"depthOffset": "depth"}).to_dict()

        return cls(
            classify=classify,
            x=gef.delivered_location.x,
            y=gef.delivered_location.y,
            z=gef.delivered_vertical_position_offset,
            name=gef.alias if gef.bro_id is None else gef.bro_id,
            groundwater_level=gef.groundwater_level_offset,
            data=data,
        )

    @classmethod
    def from_bore(cls, gef: BoreData) -> "Column":
        """
        Transform the BoreData DataClass to our Column class

        Parameters
        ----------
        gef: pygef.bore.BoreData
            Bore object created by pygef.
        Returns
        -------
        Column
        """

        classify = {
            "depth": gef.data.get_column("upperBoundaryOffset").to_list(),
            "thickness": (
                gef.data.get_column("lowerBoundary")
                - gef.data.get_column("upperBoundary")
            ).to_list(),
            "geotechnicalSoilName": gef.data.get_column(
                "geotechnicalSoilName"
            ).to_list(),
        }

        return cls(
            classify=classify,
            x=gef.delivered_location.x,
            y=gef.delivered_location.y,
            z=gef.delivered_vertical_position_offset,
            name=gef.alias if gef.bro_id is None else gef.bro_id,
            groundwater_level=gef.groundwater_level,
        )

    @property
    def x(self) -> float:
        """x coordinate"""
        return self._x

    @property
    def y(self) -> float:
        """y coordinate"""
        return self._y

    @property
    def z(self) -> Optional[float]:
        """surface level [m REF]"""
        return self._z

    @property
    def groundwater_level(self) -> Optional[float]:
        """groundwater level [m REF]"""
        return self._groundwater_level

    @property
    def name(self) -> str:
        """column name"""
        return self._name

    @property
    def classify(self) -> dict:
        """dictionary that holds the classification data"""
        return self._classify

    @property
    def data(self) -> dict:
        """dictionary that holds the other data"""
        return self._data

    def plot(
        self,
        figure: Optional[Figure] = None,
        hue: str = "percentage",
        plot_kwargs: Optional[dict] = None,
        x0: float = 0,
        d_left: float = 0.5,
        d_right: float = 0.5,
        fillpattern: bool = True,
        profile: bool = False,
    ) -> Figure:
        """
        Create a plotly figure with the Soil Layout and the Data.

        Parameters
        ----------
        figure: Figure, optional
            Default is None
            A plotly graph object.
        hue: str, optional
            default is percentage
            enum : ['percentage', 'uniform']
            Show either the soil data in percentage or use a uniform color.
        plot_kwargs: Dict, optional
            Default is None
            Dictionary with keys for properties to plot.
            Example: {
                "coneResistance": {"line_color": "black"},
                "localFriction": {"line_color": "red", "factor": 10},
            }
        x0: float, optional
            Default is 0
            The x-coordinate of the start of the Soil Layout plot
        d_left: float, optional
            Default is 0.5
            The width of the Soil Layout plot left of the center line.
            Only used when heu is not percentage. If percentage the sum of
            d_right and d_left is DEFAULT_COLUMN_WIDTH.
        d_right: float, optional
            Default is 0.5
            The width of the Soil Layout plot right of the center line.
            Only used when heu is not percentage. If percentage the sum of
            d_right and d_left is DEFAULT_COLUMN_WIDTH.
        fillpattern:  bool, optional
            Default is True
            Fill the layers with the pattern related to the soil code of the
            layer based on the NEN-EN-ISO 14688-1:2019+NEN 8990:2020 Tabel NA.17
        profile: bool, optional
            Default is False
            Flag that indicates if plot is standalone or part on of a profile.

        Returns
        -------
        Figure

        """
        if hue not in ["percentage", "uniform"]:
            raise ValueError("Invalid value for heu.")

        # with of the column
        dx = d_left + d_right
        # end of the column
        x1 = x0 + dx
        # center of the column
        x_center = x0 + d_left

        if hue == "percentage":
            # reset column to one meter width
            dx = DEFAULT_COLUMN_WIDTH
            x0 = x_center - dx / 2

        if figure is None:
            # initialize plot
            figure = make_subplots(
                rows=1,
                cols=2,
                y_title="Depth [m REF]",
                shared_yaxes=True,
                horizontal_spacing=0.01,
                column_widths=[dx, 3.5],
                subplot_titles=(
                    "Soil Layout",
                    "Data",
                ),
            )

        # Add bars for each soil type separately in order to be able to set legend labels
        for key in np.unique(self.classify["geotechnicalSoilName"]):
            # get index location of the soil code
            select = np.array(self.classify["geotechnicalSoilName"]) == key

            # illiterate of depth and add bar plot
            for y0, dy in zip(
                np.array(self.classify["depth"])[select],
                np.array(self.classify["thickness"])[select],
            ):
                # Based on the percentage of soil create the bar for every layer.
                if hue == "percentage":
                    # start of the bar per color.
                    x0_color = copy.copy(x0)
                    for i, (color, percentage) in enumerate(
                        CODING_SOIL_TYPES[key]["color"].items()
                    ):
                        # end of the bar per color.
                        x1_color = ((percentage / 100) * dx) + x0_color

                        figure.add_trace(
                            go.Scatter(
                                name=key,
                                x=[x0_color, x0_color, x1_color, x1_color, x0_color],
                                y=[y0, y0 - dy, y0 - dy, y0, y0],
                                text=(
                                    f"Name: {self.name}<br>"
                                    f"Soil Type: {key}<br>"
                                    f"Top of layer: {y0:.2f}<br>"
                                    f"Bottom of layer: {y0 - dy:.2f}<br>"
                                    f"Thickness: {dy:.2f}"
                                ),
                                hovertemplate="%{text}",
                                legendgroup=key,
                                mode="lines",
                                fill="toself",
                                fillcolor=color,
                                line=dict(color=color),
                                showlegend=key not in [i.name for i in figure.data],
                                fillpattern=(
                                    CODING_SOIL_TYPES[key]["pattern"][i]
                                    if fillpattern
                                    else None
                                ),
                            ),
                            row=1,
                            col=1,
                        )

                        # reset the start of the bar color.
                        x0_color = x1_color

                elif hue == "uniform":
                    # blend color based on the percentage
                    red = int(
                        sum(
                            [
                                ImageColor.getcolor(c, "RGB")[0] * p
                                for c, p in CODING_SOIL_TYPES[key]["color"].items()
                            ]
                        )
                        / 100
                    )
                    green = int(
                        sum(
                            [
                                ImageColor.getcolor(c, "RGB")[1] * p
                                for c, p in CODING_SOIL_TYPES[key]["color"].items()
                            ]
                        )
                        / 100
                    )
                    blue = int(
                        sum(
                            [
                                ImageColor.getcolor(c, "RGB")[2] * p  # type: ignore
                                for c, p in CODING_SOIL_TYPES[key]["color"].items()
                            ]
                        )
                        / 100
                    )
                    color = "#%02x%02x%02x" % (red, green, blue)

                    figure.add_trace(
                        go.Scatter(
                            name=key,
                            x=[x0, x0, x1, x1, x0],
                            y=[y0, y0 - dy, y0 - dy, y0, y0],
                            text=(
                                f"Name: {self.name}<br>"
                                f"Soil Type: {key}<br>"
                                f"Top of layer: {y0:.2f}<br>"
                                f"Bottom of layer: {y0 - dy:.2f}<br>"
                                f"Thickness: {dy:.2f}"
                            ),
                            hovertemplate="%{text}",
                            legendgroup=key,
                            mode="lines",
                            fill="toself",
                            fillcolor=color,
                            line=dict(color=color),
                            showlegend=key not in [i.name for i in figure.data],
                            fillpattern=(
                                CODING_SOIL_TYPES[key]["pattern"][0]
                                if fillpattern
                                else None
                            ),
                        ),
                        row=1,
                        col=1,
                    )
                else:
                    raise ValueError

        # plot other data
        if plot_kwargs is not None:
            for item in plot_kwargs.keys():
                if item not in self.data.keys():
                    logging.warning(f"{item} not in data dictionary {self.name}.")
                    continue

                # pop not needed plot kwargs
                scatter_kwargs = copy.deepcopy(plot_kwargs)
                if "factor" in scatter_kwargs[item].keys():
                    scatter_kwargs[item].pop("factor")

                # add data to column
                figure.add_trace(
                    go.Scatter(
                        name=item,
                        x=np.array(self.data[item])
                        * plot_kwargs[item].get("factor", 1.0)
                        + x_center,
                        y=self.data["depth"],
                        customdata=self.data[item],
                        hovertemplate="%{customdata:.2f}, %{y:.2f}",
                        legendgroup=item,
                        showlegend=item not in [i.name for i in figure.data],
                        **scatter_kwargs[item],
                    ),
                    row=1,
                    col=1 if profile else 2,
                )

        # Add dashed blue line representing phreatic level
        if self.groundwater_level is not None and not profile:
            figure.add_hline(
                y=self.groundwater_level,
                line=dict(color="Blue", dash="dash", width=1),
                row="all",
                col="all",
                annotation_text=f"Phreatic level [m REF]: {self.groundwater_level:.2f}",
                annotation_position="bottom right",
                annotation_font_size=10,
                annotation_font_color="black",
            )

        # Add dashed brown line representing ground level
        if self.z is not None and not profile:
            figure.add_hline(
                y=self.z,
                line=dict(color="Brown", dash="dash", width=1),
                row="all",
                col="all",
                annotation_text=f"surface level [m REF]: {self.z:.2f}",
                annotation_position="bottom right",
                annotation_font_size=10,
                annotation_font_color="black",
            )

        if not profile:
            # update figure
            figure.update_layout(title_text=f"Name: {self.name}")
            figure.update_xaxes(row=1, col=1, showticklabels=False, visible=False)

        if profile:
            # add a vertical line to locate the column on the profile
            figure.add_vline(
                x=x_center,
                line=dict(color="Black", dash="dash", width=1),
                row="all",
                col="all",
                annotation_text=self.name,
                annotation_position="top right",
                annotation_font_size=10,
                annotation_font_color="black",
                annotation_textangle=90,
            )

        return figure
