from collections import namedtuple
from pint import UnitRegistry
from functools import lru_cache
import math

ureg = UnitRegistry()
ureg.define("dollar = d")

STEEL_DENSITY = 8.05 * ureg.gram / ureg.centimeter ** 3

EDGE_LENGTH = 10 * ureg.centimeter
EDGE_DIAMETER = 3 / 8 * ureg.inch
NODE_DIAMETER = 1 * ureg.inch

NODE_VOLUME = 4/3 * math.pi * (NODE_DIAMETER/2) ** 3

NODE_WEIGHT = NODE_VOLUME * STEEL_DENSITY

EDGE_COST = 1 * ureg.dollar / ureg.foot
NODE_COST = 0.75 * ureg.dollar

Bom = namedtuple("Bom", ['edgeLength', 'nodes', 'edges'])

first = Bom(edgeLength=1, nodes=6, edges=12)


@lru_cache
def octoflake_stats(edgeLength):
    if edgeLength == 1:
        return Bom(edgeLength=1, nodes=6, edges=12)
    last = octoflake_stats(edgeLength // 2)
    next_edge_length = 2 * last.edgeLength

    naive_nodes = 6 * last.nodes
    naive_edges = 6 * last.edges

    duplicate_nodes = 6 * next_edge_length + 5
    duplicate_edges = 6 * next_edge_length

    next_nodes = naive_nodes - duplicate_nodes
    next_edges = naive_edges - duplicate_edges

    return Bom(edgeLength=next_edge_length, nodes=next_nodes, edges=next_edges)


def octoflake_cost_and_weight(edge_length):
    stats = octoflake_stats(edge_length)

    total_edge_length = (EDGE_LENGTH * stats.edges).to("feet")
    edge_cost = total_edge_length * EDGE_COST
    edge_weight = (total_edge_length * math.pi * (EDGE_DIAMETER / 2) ** 2 * STEEL_DENSITY).to("pounds")

    total_node_weight = (stats.nodes * NODE_WEIGHT).to("pounds")



    print(f"For an octoflake with {edge_length=}:")
    print(f"The {total_edge_length} of edges cost {total_edge_length} and weighs {edge_weight} ")
    print(f"The {stats.nodes} nodes weight {total_node_weight}")
    print(f"The overall weight is {edge_weight + total_node_weight}")


if __name__ == "__main__":
    print(STEEL_DENSITY)
    print(EDGE_DIAMETER)
    print(octoflake_stats(8))
    octoflake_cost_and_weight(8)

# second = nextIteration(first)
# third = nextIteration(second)
# fourth = nextIteration(third)
# fifth = nextIteration(fourth)
#
# print(first)
# print(second)
# print(third)
# print(fourth)
# print(fifth)
