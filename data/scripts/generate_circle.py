#/usr/bin/env python3
import json
import click
import numpy as np

@click.command()
@click.argument("output_fname", type=click.Path(file_okay=True, dir_okay=False))
def main(output_fname):
    steps = 180
    radius = 10

    # r**2 = x**2 + y**2 <=> y = +- sqrt(r**2 - x**2)
    x_0 = np.linspace(-radius, radius, num=steps, endpoint=True)
    x_1 = x_0[::-1]
    x = np.concatenate((x_0, x_1[1:]))

    y_0 = np.sqrt(radius**2 - x_0**2)
    y_1 = -y_0[::-1]
    y = np.concatenate((y_0, y_1[1:]))

    coords = list(zip(x, y))
    result = [
            {
                "name": "circle",
                "polygon": coords,
                "type": "plus",
            }
            ]

    with open(output_fname, "w") as f:
        json.dump(result, f, indent=4, sort_keys=True)

if __name__ == "__main__":
    main()
