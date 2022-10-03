import numpy as np


def v_to_z(v, gamma1=0.33, gamma2=3.35, max_value=3, zmin=0.06):
    norm_v = v / max_value
    term1 = 1 - norm_v * 0.6
    term1 = 2 * gamma1 / term1
    term2 = term1 - 4 + gamma2
    z = zmin / term2
    return z