import math
import re
from typing import NamedTuple, Dict, List, Tuple

INPUT = "input8.txt"
#INPUT = "testinput8.txt"
LEFT = 'L'
RIGHT = 'R'
PATTERN = r"([\dA-Z]{3}) += +\(([\dA-Z]{3}), ([\dA-Z]{3})"
START = "AAA"
END = "ZZZ"


class Node(NamedTuple):
    label: str
    left: str
    right: str


class Directions(NamedTuple):
    steps: list
    nodes: Dict[str, Node]


def get_directions() -> Directions:
    steps = []
    nodes = {}
    with open(INPUT, 'r') as f_in:
        for i, raw_line in enumerate(f_in):
            line = raw_line.strip()
            if i == 0:
                steps = [c for c in line]
            elif line:
                match = re.match(PATTERN, line)
                nodes[match.group(1)] = Node(match.group(1), match.group(2), match.group(3))
    return Directions(steps, nodes)


def main1():
    directions = get_directions()

    steps_taken = 0
    step_index = 0
    current_node = directions.nodes[START]
    while current_node.label != END:
        next_step = directions.steps[step_index]
        if next_step == LEFT:
            current_node = directions.nodes[current_node.left]
        else:
            current_node = directions.nodes[current_node.right]

        # cycle back to start
        steps_taken += 1
        step_index = steps_taken % len(directions.steps)

    print(f"Took {steps_taken} steps")


def have_finished(current_nodes: List[Node]) -> bool:
    return all(n.label.endswith('Z') for n in current_nodes)


def get_steps_to_first_z(start_node: Node, directions: Directions, offset: int = 0) -> Tuple[int, Node]:
    steps_taken = 0
    step_index = offset
    current_node = start_node
    while not current_node.label.endswith('Z') or not steps_taken:
        next_step = directions.steps[step_index]
        if next_step == LEFT:
            current_node = directions.nodes[current_node.left]
        else:
            current_node = directions.nodes[current_node.right]

        # cycle back to start
        steps_taken += 1
        step_index = steps_taken % len(directions.steps)

    print(f"Took {steps_taken} steps for node {start_node}")
    return steps_taken, current_node


# Simultaneously start on every node that ends with A.
# How many steps does it take before you're only on nodes that end with Z?
def main2():
    directions = get_directions()

    current_nodes = [n for n in directions.nodes.values() if n.label.endswith("A")]
    steps_by_node = {}
    end_nodes = []
    for n in current_nodes:
        steps, end_node = get_steps_to_first_z(n, directions)
        end_nodes.append(end_node)
        steps_by_node[n] = steps

    start_loop_steps = max(steps_by_node.values())
    offset = start_loop_steps % len(directions.steps)

    print(f"\nchecking loops")
    cycle_length = []
    for n in end_nodes:
        cycle_length.append(get_steps_to_first_z(n, directions, offset=offset)[0])

    total_steps = math.lcm(*cycle_length)
    print(f"total steps is {total_steps}")


if __name__ == "__main__":
    main2()
