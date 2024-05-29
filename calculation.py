from itertools import permutations
from collections import deque

starting_configurations = [
    ((1, 2, 3), (), ()),
    ((1, 2), (3,), ()),
    ((1,), (2,), (3,)),
]

# for the case where the pole lengths are decreasing
starting_configurations_decreasing = [
    ((1, 2, 3), (), ()),
    ((1, 2), (3,), ()),
    ((1, 2), (), (3,)),
    ((3,), (1, 2), ()),
    ((), (1, 2), (3,)),
    ((1,), (2,), (3,)),
]

# returns an iterator over the possible configurations that can be reached
# from a given configuration, in one move
def neighbours(configuration, decreasing=False):
    for (i, start), (j, end) in permutations(enumerate(configuration), 2):
        height = 3 - j if decreasing else 3
        if len(start) == 0 or len(end) == height:
            # move not possible
            continue
        # change to list to modify
        as_list = list(configuration)
        as_list[i] = start[:-1]
        as_list[j] = end + start[-1:]
        yield tuple(as_list)

# returns dictionary { configuration: (distance, configuration_before_end) }
# this is a variation on a standard algorithm, `Breadth First Search`
def get_distances(start_configuration, decreasing=False):
    q = deque([start_configuration])
    visited = { start_configuration: (0, None) }

    while q:
        # get the current configuration off the queue
        current = q.pop()
        # add one to the move count
        new_moves_count = visited[current][0] + 1
        
        for neighbour in neighbours(current, decreasing):
            if neighbour not in visited:
                q.appendleft(neighbour)
                visited[neighbour] = (new_moves_count, current)
    return visited

results = dict()
for configuration in starting_configurations:
    results[configuration] = get_distances(configuration)

results_decreasing = dict()
for configuration in starting_configurations_decreasing:
    results_decreasing[configuration] = get_distances(configuration, decreasing=True)


