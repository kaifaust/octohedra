import random
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

r = random.Random()


def simulate(initial_population,
             interaction_probability,
             replication_probability,
             replication_magnitude,
             large_number_threshold=10000,
             id_99=100000,
             time_steps=100):
    pop = initial_population
    t = 0
    yield pop
    while t < time_steps:
        if pop < large_number_threshold:
            for _ in range(pop):
                if r.random() < interaction_probability:
                    pop += replication_magnitude if r.random() < replication_probability else -1
        elif pop < id_99:
            pop = round(pop * (1 - interaction_probability) + (
                    replication_magnitude * replication_probability * pop *
                    interaction_probability))
        else:
            pop = id_99
        t += 1
        yield min(pop, id_99)


time_steps = 50
interaction_probability = 0.25
destruction_probability = 0.1

fig, axs = plt.subplots(3, 3)
for i, initial in enumerate((100, 1000, 2000)):
    for j, variance in enumerate((10, 100, 1000)):

        print(1 / variance)
        x = [[pop for pop in
              simulate(initial,
                       interaction_probability,
                       1 / variance,
                       round(2 * variance),
                       time_steps=time_steps)
              ] for _
             in range(1000)]

        x = np.array(x)
        counter = Counter(x[:, -1])
        print(initial, variance, counter)
        x = x.transpose()
        axs[i, j].semilogy(range(time_steps + 1), x)
        axs[i, j].set_title(f"pop: {initial}, var: {variance}")

for ax in axs.flat:
    ax.label_outer()
fig.tight_layout()
plt.show()
