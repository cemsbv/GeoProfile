from plotly.graph_objs import Figure

from geoprofile import Column


def test_column_plot(classify_dict: dict, data_dict: dict) -> None:
    column = Column(classify_dict, 0, 0)
    assert isinstance(column.plot(), Figure)

    column = Column(classify_dict, 0, 0, data=data_dict)

    # test factor
    assert isinstance(
        column.plot(
            plot_kwargs={
                "qc": {"line_color": "black"},
                "fs": {"line_color": "red", "factor": 10},
            }
        ),
        Figure,
    )
