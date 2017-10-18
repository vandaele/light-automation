from random import randint


def random6():
    regs_values = [0] * 23
    indices = []
    while len(indices) < 6:
        val = randint(0, 22)
        print val
        if val not in indices:
            indices.append(val)
            regs_values[val] = 100
    return regs_values