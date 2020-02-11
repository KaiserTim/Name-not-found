#!/usr/bin/env python3
import os
import json
import click
from shapely.geometry import Polygon
from descartes import PolygonPatch
import matplotlib.pyplot as plt

@click.command()
@click.argument("input-fname", type=click.Path(exists=True, file_okay=True, dir_okay=False))
def main(input_fname):
    with open(input_fname, "r") as f:
        content = json.load(f)

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    fig, ax = plt.subplots(1, 1)
    for i, item in enumerate(content):
        color = colors[i % len(colors)]
        ax.add_patch(PolygonPatch(Polygon(item["polygon"]), fc=color))
    ax.set_title(os.path.basename(input_fname))
    ax.set_aspect("equal")
    ax.autoscale()
    plt.show()

if __name__ == "__main__":
    main()
