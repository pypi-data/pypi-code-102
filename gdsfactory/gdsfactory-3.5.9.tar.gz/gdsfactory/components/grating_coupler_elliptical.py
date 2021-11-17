from typing import Optional, Tuple

import numpy as np
from numpy import ndarray

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.geometry.functions import DEG2RAD, extrude_path
from gdsfactory.tech import LAYER
from gdsfactory.types import Layer


def ellipse_arc(
    a: float,
    b: float,
    x0: float,
    theta_min: float,
    theta_max: float,
    angle_step: float = 0.5,
) -> ndarray:
    """Returns an elliptical arc.

    b = a *sqrt(1-e**2)

    An ellipse with a = b has zero eccentricity (is a circle)

    Args:
        a: ellipse semi-major axis
        b: semi-minor axis

    """
    theta = np.arange(theta_min, theta_max + angle_step, angle_step) * DEG2RAD
    xs = a * np.cos(theta) + x0
    ys = b * np.sin(theta)
    return np.column_stack([xs, ys])


def grating_tooth_points(
    ap: float,
    bp: float,
    xp: float,
    width: float,
    taper_angle: float,
    spiked: bool = True,
    angle_step: float = 1.0,
) -> ndarray:
    theta_min = -taper_angle / 2
    theta_max = taper_angle / 2

    backbone_points = ellipse_arc(ap, bp, xp, theta_min, theta_max, angle_step)
    if spiked:
        spike_length = width / 3
    else:
        spike_length = 0.0
    points = extrude_path(
        backbone_points,
        width,
        with_manhattan_facing_angles=False,
        spike_length=spike_length,
    )

    return points


def grating_taper_points(
    a: float,
    b: float,
    x0: float,
    taper_length: float,
    taper_angle: float,
    wg_width: float,
    angle_step: float = 1.0,
) -> ndarray:
    taper_arc = ellipse_arc(a, b, taper_length, -taper_angle / 2, taper_angle / 2)

    port_position = np.array((x0, 0))
    p0 = port_position + (0, wg_width / 2)
    p1 = port_position + (0, -wg_width / 2)
    points = np.vstack([p0, p1, taper_arc])
    return points


@gf.cell
def grating_coupler_elliptical(
    polarization: str = "te",
    taper_length: float = 16.6,
    taper_angle: float = 40.0,
    wavelength: float = 1.554,
    fiber_angle: float = 15.0,
    grating_line_width: float = 0.343,
    wg_width: float = 0.5,
    neff: float = 2.638,  # tooth effective index
    nclad: float = 1.443,
    layer: Tuple[int, int] = LAYER.WG,
    p_start: int = 26,
    n_periods: int = 30,
    big_last_tooth: bool = False,
    layer_slab: Optional[Tuple[int, int]] = LAYER.SLAB150,
    fiber_marker_width: float = 11.0,
    fiber_marker_layer: Optional[Layer] = gf.LAYER.TE,
    spiked: bool = True,
) -> Component:
    r"""Grating coupler with parametrization based on Lumerical FDTD simulation.

    Args:
        polarization: te or tm
        taper_length: taper length from input
        taper_angle: grating flare angle
        wavelength: grating transmission central wavelength (um)
        fiber_angle: fibre angle in degrees determines ellipticity
        grating_line_width
        wg_width: waveguide width
        neff: tooth effective index
        layer: LAYER.WG
        p_start: period start first grating teeth
        n_periods: number of periods
        big_last_tooth: adds a big_last_tooth
        layer_slab
        fiber_marker_layer: Optional circular marker
        fiber_marker_width: width
        nclad
        spiked: grating teeth have sharp spikes to avoid non-manhattan drc errors


    .. code::

                      fiber

                   /  /  /  /
                  /  /  /  /
                _|-|_|-|_|-|___
        WG  o1  ______________|
    """

    # Compute some ellipse parameters
    sthc = np.sin(fiber_angle * DEG2RAD)
    d = neff ** 2 - nclad ** 2 * sthc ** 2
    a1 = wavelength * neff / d
    b1 = wavelength / np.sqrt(d)
    x1 = wavelength * nclad * sthc / d

    a1 = round(a1, 3)
    b1 = round(b1, 3)
    x1 = round(x1, 3)

    period = a1 + x1

    c = gf.Component()
    c.info.polarization = polarization
    c.info.wavelength = wavelength

    # Make each grating line
    for p in range(p_start, p_start + n_periods + 1):
        pts = grating_tooth_points(
            p * a1, p * b1, p * x1, grating_line_width, taper_angle, spiked=spiked
        )
        c.add_polygon(pts, layer)

    # Make the taper
    p_taper = p_start - 1
    p_taper_eff = p_taper
    a_taper = a1 * p_taper_eff
    b_taper = b1 * p_taper_eff
    x_taper = x1 * p_taper_eff

    x_output = a_taper + x_taper - taper_length + grating_line_width / 2
    pts = grating_taper_points(
        a_taper, b_taper, x_output, x_taper, taper_angle, wg_width=wg_width
    )
    c.add_polygon(pts, layer)

    # Superimpose a tooth without spikes at end of taper to match the period.
    pts = grating_tooth_points(
        a_taper, b_taper, x_taper, grating_line_width, taper_angle, spiked=spiked
    )
    c.add_polygon(pts, layer)

    # Add last "large tooth" after the standard grating teeth
    w = 1.0
    total_length = (
        period * (p_start + n_periods)
        + grating_line_width / 2
        + period
        - grating_line_width
        + w / 2
    )

    if big_last_tooth:
        a = total_length / (1 + x1 / a1)
        b = b1 / a1 * a
        x = x1 / a1 * a

        pts = grating_tooth_points(a, b, x, w, taper_angle, spiked=False)
        c.add_polygon(pts, layer)

    x = np.round(taper_length + period * n_periods / 2, 3)
    if fiber_marker_layer:
        circle = gf.components.circle(
            radius=fiber_marker_width / 2, layer=fiber_marker_layer
        )
        circle_ref = c.add_ref(circle)
        circle_ref.movex(x)

    name = f"vertical_{polarization.lower()}"

    c.add_port(
        name=name,
        midpoint=[x, 0],
        width=fiber_marker_width,
        orientation=0,
        layer=fiber_marker_layer,
        port_type=name,
    )

    c.add_port(
        name="o1", midpoint=[x_output, 0], width=wg_width, orientation=180, layer=layer
    )

    # Add shallow etch
    slab_length = total_length + grating_line_width + 2.0
    slab_width = slab_length * np.tan(fiber_angle * DEG2RAD) + 2.0

    if layer_slab:
        c.add_polygon(
            [
                (0, slab_width),
                (slab_length, slab_width),
                (slab_length, -slab_width),
                (0, -slab_width),
            ],
            layer_slab,
        )

    return c


grating_coupler_elliptical_tm = gf.partial(
    grating_coupler_elliptical,
    grating_line_width=0.707,
    fiber_marker_layer=gf.LAYER.TM,
    polarization="tm",
    neff=1.8,
    n_periods=16,
)


grating_coupler_elliptical_te = grating_coupler_elliptical


if __name__ == "__main__":
    # c = grating_coupler_elliptical_tm()
    # c = grating_coupler_elliptical_te(layer_slab=None, with_fiber_marker=False)
    c = grating_coupler_elliptical()
    # print(c.polarization)
    # print(c.wavelength)
    # print(c.ports)
    c.pprint()
    c.show()
