import numpy as np


def mag2db(x):
    return 20 * np.log10(x)


def db2mag(x):
    return 10 ** (x / 20)


def pwr2db(x):
    return 10 * np.log10(x)


def db2pwr(x):
    return 10 ** (x / 10)
