from pathlib import Path
import json
import matplotlib as mpl
from cycler import cycler


def load_colorscheme(
    name, background="background", foreground="foreground", grid="cyan"
):
    definition = json.loads(
        (Path("iTerm2-Color-Schemes") / "windowsterminal" / f"{name}.json").read_bytes()
    )
    mpl.rcParams["axes.edgecolor"] = definition[grid].lstrip("#")
    mpl.rcParams["grid.color"] = definition[grid].lstrip("#")
    mpl.rcParams["patch.facecolor"] = definition[grid].lstrip("#")
    mpl.rcParams["figure.facecolor"] = definition[background].lstrip("#")
    mpl.rcParams["axes.facecolor"] = definition[background].lstrip("#")
    mpl.rcParams["legend.facecolor"] = definition[background].lstrip("#")
    mpl.rcParams["legend.edgecolor"] = definition[grid].lstrip("#")
    mpl.rcParams["text.color"] = definition[foreground].lstrip("#")

    colors = (
        definition[c]
        for c in [
            "red",
            "blue",
            "yellow",
            "green",
            "purple",
            "cyan",
            "brightRed",
            "brightGreen",
            "brightPurple",
            "brightCyan",
        ]
        if definition[c] not in (definition[grid], definition[background])
    )

    mpl.rcParams["axes.prop_cycle"] = cycler(color=colors)
