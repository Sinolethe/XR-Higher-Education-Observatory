# src/utils.py

PLATFORM = [
    "Quest",
    "HoloLens",
    "PCVR",
    "WebXR",
    "Mobile AR"
]

XR_TYPE = [
    "VR",
    "AR",
    "MR",
    "XR",
    "Spatial Computing"
]


def validate(project):

    if project["technology"]["platform"] not in PLATFORM:
        raise ValueError(
            f'Invalid platform: {project["technology"]["platform"]}'
        )

    if project["technology"]["xr_type"] not in XR_TYPE:
        raise ValueError(
            f'Invalid XR type: {project["technology"]["xr_type"]}'
        )

    return True
