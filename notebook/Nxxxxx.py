import plotly
import plotly.io as pio
import pygef
from nuclei.client import NucleiClient
from shapely.geometry import LineString
from tqdm import tqdm

from geoprofilecore import Column, Section

pio.renderers.default = "browser"

client = NucleiClient()

author = "N. Uclei"
project_name = "Profile"
project_number = "6169"
profile_line = LineString([[125015, 477692], [127464, 470809], [127603, 464535]])


# get all project ID's
projects = client.session.get(
    url="https://datalake.cemsbv.io/datalake/api/v1/admin/projects"
)

# find project ID of your project name
project_id = [i["id"] for i in projects.json() if i["number"] == str(project_number)][0]

# get all files metadata related to your project
files = client.session.get(
    url=f"https://datalake.cemsbv.io/datalake/api/v1/admin/projects/{project_id}/files"
)

# loop over the files metadata and fetch file from DataLake
cpt_files = []
for file in tqdm(files.json()):
    # only download application/cpt files
    if file["mime"].startswith("application/cpt"):
        cpt_files.append(
            client.session.get(
                url=f'https://datalake.cemsbv.io/datalake/api/v1/admin/files/{file["id"]}'
            ).text
        )

# create columns
columns = []
for file in tqdm(cpt_files):
    # parse GEF file
    gef = pygef.read_cpt(file)

    # drop non-unique elements
    data = gef.data.unique(subset="penetrationLength", maintain_order=True)

    # create schema for cpt classification
    schema = {
        "aggregateLayersPenalty": 3,
        "data": {
            "coneResistance": data.get_column("coneResistance").to_list(),
            "correctedPenetrationLength": data.get_column(
                "penetrationLength"
            ).to_list(),
            "localFriction": data.get_column("localFriction").clip(0, 1e10).to_list(),
        },
        "verticalPositionOffset": gef.delivered_vertical_position_offset,
        "x": gef.delivered_location.x,
        "y": gef.delivered_location.y,
    }
    response = client.session.post(
        "https://crux-nuclei.com/api/cptcore/v1/classify/machineLearning",
        json=schema,
        headers={"Content-Type": "application/json"},
    )

    if response.status_code != 200:
        print(response.content)

    columns.append(Column.from_cpt(response.json(), gef))

profile = Section(
    columns,
    sorting_algorithm="nearest_neighbor",
    profile_line=profile_line,
    buffer=200,
    reproject=True,
)

# create a map of the line and CPT's
profile.plot_map(add_basemap=False, add_tags=True, debug=True)


# create a profile
fig = profile.plot(
    plot_kwargs={
        "coneResistance": {"line_color": "black"},
        "localFriction": {"line_color": "red", "factor": 10},
    },
    hue="uniform",
    fillpattern=False,
    surface_level=True,
    groundwater_level=True,
)
# html file
_ = plotly.offline.plot(fig, filename=project_number + " " + project_name + ".html")

# png file
fig.update_layout(showlegend=False)
# fig.write_image("profile_A2.png", width=1900, height=937)
