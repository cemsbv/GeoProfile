from typing import Any, Dict

KEIEN_COLOR = "#ffffff"  # wit
KEITJES_COLOR = "#ffffff"  # wit
GRIND_COLOR = "#FFA500"  # oranje
ZAND_COLOR = "#FFFF00"  # geel
SILT_COLOR = "#808080"  # grijs
KLEI_COLOR = "#008000"  # groen
VEEN_COLOR = "#964B00"  # bruin
DETRITUS_COLOR = VEEN_COLOR
HUMUS_COLOR = VEEN_COLOR
BRUINKOOL_COLOR = VEEN_COLOR
GYTTJA_COLOR = VEEN_COLOR
NOT_DEFINED_COLOR = "#FF0000"  # red

KEIEN_PATTERN: Dict[str, str] = {}
KEITJES_PATTERN: Dict[str, str] = {}
GRIND_PATTERN = {"shape": "."}
ZAND_PATTERN = {"shape": "."}
SILT_PATTERN = {"shape": "|"}
KLEI_PATTERN = {"shape": "/"}
VEEN_PATTERN = {"shape": "-"}
DETRITUS_PATTERN = VEEN_PATTERN
HUMUS_PATTERN = VEEN_PATTERN
BRUINKOOL_PATTERN = VEEN_PATTERN
GYTTJA_PATTERN = VEEN_PATTERN
NOT_DEFINED_PATTERN = {"shape": "+"}

# NEN-EN-ISO 14688-1:2019+NEN 8990:2020
# Tabel NA.17
CODING_SOIL_TYPES: Dict[str, Dict[str, Any]] = {
    "keien": {"color": {KEIEN_COLOR: 100}, "pattern": [KEIEN_PATTERN]},
    "keienMetGrind": {
        "color": {KEIEN_COLOR: 80, GRIND_COLOR: 20},
        "pattern": [KEIEN_PATTERN, GRIND_PATTERN],
    },
    "keienMetZand": {
        "color": {KEIEN_COLOR: 80, ZAND_COLOR: 20},
        "pattern": [KEIEN_PATTERN, ZAND_PATTERN],
    },
    "keienMetSilt": {
        "color": {KEIEN_COLOR: 80, SILT_COLOR: 20},
        "pattern": [KEIEN_PATTERN, SILT_PATTERN],
    },
    "keienMetKlei": {
        "color": {KEIEN_COLOR: 80, KLEI_COLOR: 20},
        "pattern": [KEIEN_PATTERN, KLEI_PATTERN],
    },
    "keitjes": {"color": {KEITJES_COLOR: 100}, "pattern": [KEITJES_PATTERN]},
    "keitjesMetGrind": {
        "color": {KEITJES_COLOR: 80, GRIND_COLOR: 20},
        "pattern": [KEITJES_PATTERN, GRIND_PATTERN],
    },
    "keitjesMetZand": {
        "color": {KEITJES_COLOR: 80, ZAND_COLOR: 20},
        "pattern": [KEITJES_PATTERN, ZAND_PATTERN],
    },
    "keitjesMetSilt": {
        "color": {KEITJES_COLOR: 80, SILT_COLOR: 20},
        "pattern": [KEITJES_PATTERN, SILT_PATTERN],
    },
    "keitjesMetKlei": {
        "color": {KEITJES_COLOR: 80, KLEI_COLOR: 20},
        "pattern": [KEITJES_PATTERN, KLEI_PATTERN],
    },
    "grind": {"color": {GRIND_COLOR: 100}, "pattern": [GRIND_PATTERN]},
    "grindMetKeien": {
        "color": {GRIND_COLOR: 80, KEIEN_COLOR: 20},
        "pattern": [GRIND_PATTERN, KEIEN_PATTERN],
    },
    "grindMetKeitjes": {
        "color": {GRIND_COLOR: 80, KEITJES_COLOR: 20},
        "pattern": [GRIND_PATTERN, KEITJES_PATTERN],
    },
    "zwakZandigGrind": {
        "color": {GRIND_COLOR: 90, ZAND_COLOR: 10},
        "pattern": [GRIND_PATTERN, ZAND_PATTERN],
    },
    "sterkZandigGrind": {
        "color": {GRIND_COLOR: 70, ZAND_COLOR: 30},
        "pattern": [GRIND_PATTERN, ZAND_PATTERN],
    },
    "siltigGrind": {
        "color": {GRIND_COLOR: 80, SILT_COLOR: 20},
        "pattern": [GRIND_PATTERN, SILT_PATTERN],
    },
    "kleiigGrind": {
        "color": {GRIND_COLOR: 80, KLEI_COLOR: 20},
        "pattern": [GRIND_PATTERN, KLEI_PATTERN],
    },
    "zand": {"color": {ZAND_COLOR: 100}, "pattern": [ZAND_PATTERN]},
    "zandMetKeien": {
        "color": {ZAND_COLOR: 80, KEIEN_COLOR: 20},
        "pattern": [ZAND_PATTERN, KEIEN_PATTERN],
    },
    "zandMetKeitjes": {
        "color": {ZAND_COLOR: 80, KEITJES_COLOR: 20},
        "pattern": [ZAND_PATTERN, KEITJES_PATTERN],
    },
    "zwakGrindigZand": {
        "color": {ZAND_COLOR: 90, GRIND_COLOR: 10},
        "pattern": [ZAND_PATTERN, GRIND_PATTERN],
    },
    "sterkGrindigZand": {
        "color": {ZAND_COLOR: 70, GRIND_COLOR: 30},
        "pattern": [ZAND_PATTERN, GRIND_PATTERN],
    },
    "siltigZand": {
        "color": {ZAND_COLOR: 80, SILT_COLOR: 20},
        "pattern": [ZAND_PATTERN, SILT_PATTERN],
    },
    "siltigZandMetGrind": {
        "color": {ZAND_COLOR: 80, SILT_COLOR: 20},
        "pattern": [ZAND_PATTERN, SILT_PATTERN],
    },
    "kleiigZand": {
        "color": {ZAND_COLOR: 80, KLEI_COLOR: 20},
        "pattern": [ZAND_PATTERN, KLEI_PATTERN],
    },
    "kleiigZandMetGrind": {
        "color": {ZAND_COLOR: 80, KLEI_COLOR: 20},
        "pattern": [ZAND_PATTERN, KLEI_PATTERN],
    },
    "silt": {"color": {SILT_COLOR: 100}, "pattern": [SILT_PATTERN]},
    "siltMetKeien": {
        "color": {SILT_COLOR: 80, KEIEN_COLOR: 20},
        "pattern": [SILT_PATTERN, KEIEN_PATTERN],
    },
    "siltMetKeitjes": {
        "color": {SILT_COLOR: 80, KEITJES_COLOR: 20},
        "pattern": [SILT_PATTERN, KEITJES_PATTERN],
    },
    "zwakGrindigSilt": {
        "color": {SILT_COLOR: 90, GRIND_COLOR: 10},
        "pattern": [SILT_PATTERN, GRIND_PATTERN],
    },
    "sterkGrindigSilt": {
        "color": {SILT_COLOR: 70, GRIND_COLOR: 30},
        "pattern": [SILT_PATTERN, GRIND_PATTERN],
    },
    "zwakZandigSilt": {
        "color": {SILT_COLOR: 90, ZAND_COLOR: 10},
        "pattern": [SILT_PATTERN, ZAND_PATTERN],
    },
    "zwakZandigSiltMetGrind": {
        "color": {SILT_COLOR: 90, ZAND_COLOR: 10},
        "pattern": [SILT_PATTERN, ZAND_PATTERN],
    },
    "sterkZandigSilt": {
        "color": {SILT_COLOR: 70, ZAND_COLOR: 30},
        "pattern": [SILT_PATTERN, ZAND_PATTERN],
    },
    "sterkZandigSiltMetGrind": {
        "color": {SILT_COLOR: 70, ZAND_COLOR: 30},
        "pattern": [SILT_PATTERN, ZAND_PATTERN],
    },
    "klei": {"color": {KLEI_COLOR: 100}, "pattern": [KLEI_PATTERN]},
    "kleiMetKeien": {
        "color": {KLEI_COLOR: 80, KEIEN_COLOR: 20},
        "pattern": [KLEI_PATTERN, KEIEN_PATTERN],
    },
    "kleiMetKeitjes": {
        "color": {KLEI_COLOR: 80, KEIEN_COLOR: 20},
        "pattern": [KLEI_PATTERN, KEIEN_PATTERN],
    },
    "zwakGrindigeKlei": {
        "color": {KLEI_COLOR: 90, GRIND_COLOR: 10},
        "pattern": [KLEI_PATTERN, GRIND_PATTERN],
    },
    "sterkGrindigeKlei": {
        "color": {KLEI_COLOR: 70, GRIND_COLOR: 30},
        "pattern": [KLEI_PATTERN, GRIND_PATTERN],
    },
    "zwakZandigeKlei": {
        "color": {KLEI_COLOR: 90, ZAND_COLOR: 10},
        "pattern": [KLEI_PATTERN, ZAND_PATTERN],
    },
    "zwakZandigeKleiMetGrind": {
        "color": {KLEI_COLOR: 90, ZAND_COLOR: 10},
        "pattern": [KLEI_PATTERN, ZAND_PATTERN],
    },
    "sterkZandigeKlei": {
        "color": {KLEI_COLOR: 70, ZAND_COLOR: 30},
        "pattern": [KLEI_PATTERN, ZAND_PATTERN],
    },
    "sterkZandigeKleiMetGrind": {
        "color": {KLEI_COLOR: 70, ZAND_COLOR: 30},
        "pattern": [KLEI_PATTERN, ZAND_PATTERN],
    },
    "organischKlei": {  # not in NEN-EN-ISO 14688-1:2019+NEN 8990:2020, here for compatibility with the NEN9997-1
        "color": {KLEI_COLOR: 80, HUMUS_COLOR: 20},
        "pattern": [KLEI_PATTERN, HUMUS_COLOR],
    },
    "detritus": {"color": {DETRITUS_COLOR: 100}, "pattern": [DETRITUS_PATTERN]},
    "zwakZandigeDetritus": {
        "color": {DETRITUS_COLOR: 90, ZAND_COLOR: 10},
        "pattern": [DETRITUS_PATTERN, ZAND_PATTERN],
    },
    "sterkZandigeDetritus": {
        "color": {DETRITUS_COLOR: 70, ZAND_COLOR: 30},
        "pattern": [DETRITUS_PATTERN, ZAND_PATTERN],
    },
    "siltigeDetritus": {
        "color": {DETRITUS_COLOR: 80, SILT_COLOR: 20},
        "pattern": [DETRITUS_PATTERN, SILT_PATTERN],
    },
    "kleiigeDetritus": {
        "color": {DETRITUS_COLOR: 80, KLEI_COLOR: 20},
        "pattern": [DETRITUS_PATTERN, KLEI_PATTERN],
    },
    "humus": {"color": {HUMUS_COLOR: 100}, "pattern": [HUMUS_PATTERN]},
    "zwakZandigeHumus": {
        "color": {HUMUS_COLOR: 90, ZAND_COLOR: 10},
        "pattern": [HUMUS_PATTERN, ZAND_PATTERN],
    },
    "sterkZandigeHumus": {
        "color": {HUMUS_COLOR: 70, ZAND_COLOR: 30},
        "pattern": [HUMUS_PATTERN, ZAND_PATTERN],
    },
    "siltigeHumus": {
        "color": {HUMUS_COLOR: 80, SILT_COLOR: 20},
        "pattern": [HUMUS_PATTERN, SILT_PATTERN],
    },
    "kleiigeHumus": {
        "color": {HUMUS_COLOR: 80, KLEI_COLOR: 20},
        "pattern": [HUMUS_PATTERN, KLEI_PATTERN],
    },
    "veen": {"color": {VEEN_COLOR: 100}, "pattern": [VEEN_PATTERN]},
    "zwakZandigVeen": {
        "color": {VEEN_COLOR: 90, ZAND_COLOR: 10},
        "pattern": [VEEN_PATTERN, ZAND_PATTERN],
    },
    "sterkZandigVeen": {
        "color": {VEEN_COLOR: 70, ZAND_COLOR: 30},
        "pattern": [VEEN_PATTERN, ZAND_PATTERN],
    },
    "siltigVeen": {
        "color": {VEEN_COLOR: 80, SILT_COLOR: 20},
        "pattern": [VEEN_PATTERN, SILT_PATTERN],
    },
    "kleiigVeen": {
        "color": {VEEN_COLOR: 80, KLEI_COLOR: 20},
        "pattern": [VEEN_PATTERN, KLEI_PATTERN],
    },
    "bruinkool": {"color": {BRUINKOOL_COLOR: 100}, "pattern": [BRUINKOOL_PATTERN]},
    "gyttja": {"color": {GYTTJA_COLOR: 100}, "pattern": [GYTTJA_PATTERN]},
    "niet gedefinieerd": {
        "color": {NOT_DEFINED_COLOR: 100},
        "pattern": [NOT_DEFINED_PATTERN],
    },
}

CODING_SOIL_TYPES["blokken"] = CODING_SOIL_TYPES["keien"]
CODING_SOIL_TYPES["keienNietGespecificeerd"] = CODING_SOIL_TYPES["keien"]

CODING_SOIL_TYPES["keitjesNietGespecificeerd"] = CODING_SOIL_TYPES["keitjes"]

CODING_SOIL_TYPES["matigZandigGrind"] = CODING_SOIL_TYPES["zwakZandigGrind"]
CODING_SOIL_TYPES["uiterstZandigGrind"] = CODING_SOIL_TYPES["sterkZandigGrind"]

CODING_SOIL_TYPES["zwakSiltigZand"] = CODING_SOIL_TYPES["siltigZand"]
CODING_SOIL_TYPES["matigSiltigZand"] = CODING_SOIL_TYPES["siltigZand"]
CODING_SOIL_TYPES["sterkSiltigZand"] = CODING_SOIL_TYPES["siltigZand"]
CODING_SOIL_TYPES["uiterstSiltigZand"] = CODING_SOIL_TYPES["siltigZand"]

CODING_SOIL_TYPES["matigZandigeKlei"] = CODING_SOIL_TYPES["zwakZandigeKlei"]
CODING_SOIL_TYPES["matigSiltigeKlei"] = CODING_SOIL_TYPES["zwakZandigeKlei"]
CODING_SOIL_TYPES["uiterstSiltigeKlei"] = CODING_SOIL_TYPES["zwakZandigeKlei"]
CODING_SOIL_TYPES["sterkSiltigeKlei"] = CODING_SOIL_TYPES["zwakZandigeKlei"]
CODING_SOIL_TYPES["zwakSiltigeKlei"] = CODING_SOIL_TYPES["zwakZandigeKlei"]
CODING_SOIL_TYPES["sterkZandigeLeem"] = CODING_SOIL_TYPES["zwakZandigeKlei"]
CODING_SOIL_TYPES["zwakZandigeLeem"] = CODING_SOIL_TYPES["zwakZandigeKlei"]

CODING_SOIL_TYPES["detritusNietGespecificeerd"] = CODING_SOIL_TYPES["detritus"]

CODING_SOIL_TYPES["zwakKleiigVeen"] = CODING_SOIL_TYPES["kleiigVeen"]
CODING_SOIL_TYPES["zwakKleiigVeen"] = CODING_SOIL_TYPES["kleiigVeen"]
CODING_SOIL_TYPES["sterkKleiigVeen"] = CODING_SOIL_TYPES["kleiigVeen"]
CODING_SOIL_TYPES["mineraalarmVeen"] = CODING_SOIL_TYPES["kleiigVeen"]

CODING_SOIL_TYPES["gyttjaNietGespecificeerd"] = CODING_SOIL_TYPES["gyttja"]
CODING_SOIL_TYPES["dy"] = CODING_SOIL_TYPES["gyttja"]
CODING_SOIL_TYPES["bruinkoolNietGespecificeerd"] = CODING_SOIL_TYPES["gyttja"]

CODING_SOIL_TYPES["unknown"] = CODING_SOIL_TYPES["niet gedefinieerd"]
CODING_SOIL_TYPES["Not defined"] = CODING_SOIL_TYPES["niet gedefinieerd"]
CODING_SOIL_TYPES["antropogeen"] = CODING_SOIL_TYPES["niet gedefinieerd"]
