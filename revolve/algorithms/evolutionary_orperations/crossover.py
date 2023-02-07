import random
from typing import Tuple
from copy import deepcopy
from revolve.architectures.base import Chromosome


def uniform_crossover(
    parents: Tuple[Chromosome],
    probability: float,
) -> Chromosome:
    """
    Performs uniform crossover on the given parents to produce an offspring.

    Parameters:
    parent1 (list): The first parent.
    parent2 (list): The second parent.

    Returns:
    list: The offspring produced by the crossover.
    """

    parent1, parent2 = parents

    offspring = deepcopy(parent1)

    offspring.genes = [
        parent1.genes[i] if random.random() < probability else parent2.genes[i]
        for i in range(len(parent1.genes))
    ]

    return offspring
