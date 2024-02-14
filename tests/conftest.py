"""conftest file fore shared pytest fixtures"""

import pytest


@pytest.fixture
def classify_dict() -> dict:
    classify_dict = {
        "depth": [5, -10, -20, -30],
        "thickness": [15, 10, 10, 10],
        "geotechnicalSoilName": [
            "sterkGrindigZand",
            "zwakZandigSiltMetGrind",
            "sterkZandigeDetritus",
            "grind",
        ],
    }
    return classify_dict


@pytest.fixture
def data_dict() -> dict:
    data_dict = {
        "depth": [5, -10, -20, -30],
        "qc": [0, 10, 7, 8],
        "fs": [0.5, 0.004, 1, 0.7],
    }
    return data_dict
