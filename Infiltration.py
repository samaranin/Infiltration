import numpy as np

k_i = np.array([0.20, 0.22, 0.78, 0.80,
                0.30, 0.32, 0.96, 1.00,
                1.20, 1.43, 1.80, 1.88,
                0.40, 0.50, 3.24, 3.50,
                0.38, 0.43, 2.24, 4.90,
                0.40, 0.44, 1.22, 4.00,
                0.39, 0.44, 0.96, 1.80,
                0.39, 0.45, 0.80, 1.60,
                0.40, 0.47, 0.60, 1.60], dtype=float)

c_i = np.linspace(0, 160, 9)
t_i = np.array([16, 25, 50, 75], dtype=float)

def phi_ij(c_i, c_j, t_i, t_j):
    return np.sqrt(1 + (c_i - c_j)**2 + (t_i - t_j)**2)

def calculate_aj():
    pass