import math

from pint import UnitRegistry

ureg = UnitRegistry()


def flange_holding_torque(od, id, clamping_force, cof=0.5):
    # Assuming that the clamping force is applied evenly across the annulus
    outer_radius = od / 2
    inner_radius = id / 2

    contact_area = math.pi * (outer_radius ** 2 - inner_radius ** 2)
    contact_pressure = clamping_force / contact_area
    force_per_area = cof * contact_pressure

    return (2 / 3 * math.pi * force_per_area * (outer_radius ** 3 - inner_radius ** 3)).to("newton meter")


def twisting_moment(weight, offset):
    return (weight * ureg.gravity * offset).to("newton meters")


# Bolt max clamping force from https://www.portlandbolt.com/technical/bolt-torque-chart/

print(
    flange_holding_torque(
        od=2 * ureg.inch,  # Assuming that the force is concentrated around the bolt and doesn't extend to the edges
        id=3 / 4 * ureg.inch,
        clamping_force=21800 * ureg.pounds * ureg.gravity
    )
)

print(
    twisting_moment(
        weight=100 * ureg.pounds,
        offset=2 * ureg.feet
    )
)
