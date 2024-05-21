
# External Packages | NumPy
import numpy as np

# External Packages | Numba
from numba import njit, prange

from UVA_Analysis.spinquest_gui.modules.calculations.DataOrganizer import DataOrganizer

# Define the standalone functions
@njit
def lorentz_dot(a, b):
    metric = np.array([-1, -1, -1, 1])  # Lorentzian metric signature (+, -, -, -)
    return np.dot(a * metric, b)

@njit
def boost(vector, boost_v):
    bx, by, bz = boost_v[0], boost_v[1], boost_v[2]
    b2 = bx ** 2 + by ** 2 + bz ** 2
    ggamma = 1.0 / np.sqrt(1.0 - b2)
    bp = bx * vector[0] + by * vector[1] + bz * vector[2]
    gamma2 = (ggamma - 1.0) / b2

    vector[0] += gamma2 * bp * bx + ggamma * bx * vector[3]
    vector[1] += gamma2 * bp * by + ggamma * by * vector[3]
    vector[2] += gamma2 * bp * bz + ggamma * bz * vector[3]
    vector[3] = ggamma * (vector[3] + bp)

    return vector

@njit(parallel=True)
def calcVariables(mom):
    mmu = 0.10566
    mp = 0.938
    ebeam = 120.0
    p_beam = np.array([0.0, 0.0, np.sqrt(ebeam * ebeam - mp * mp), ebeam])
    p_target = np.array([0.0, 0.0, 0.0, mp])
    p_cms = p_beam + p_target
    bv_cms = np.array([p_cms[0] / p_cms[3], p_cms[1] / p_cms[3], p_cms[2] / p_cms[3]])
    s = lorentz_dot(p_cms, p_cms)

    n_events = mom.shape[0]
    mass = np.zeros(n_events)
    pT = np.zeros(n_events)
    x1 = np.zeros(n_events)
    x2 = np.zeros(n_events)
    xF = np.zeros(n_events)
    costheta = np.zeros(n_events)
    sintheta = np.zeros(n_events)
    phi = np.zeros(n_events)

    for i in prange(n_events):
        momentum = mom[i]
        E_pos = np.sqrt(momentum[0] * momentum[0] + momentum[1] * momentum[1] + momentum[2] * momentum[2] + mmu * mmu)
        p_pos = np.array([momentum[0], momentum[1], momentum[2], E_pos])
        E_neg = np.sqrt(momentum[3] * momentum[3] + momentum[4] * momentum[4] + momentum[5] * momentum[5] + mmu * mmu)
        p_neg = np.array([momentum[3], momentum[4], momentum[5], E_neg])

        p_sum = p_pos + p_neg

        mass[i] = np.sqrt(lorentz_dot(p_sum, p_sum))
        pT[i] = np.sqrt(p_sum[0] ** 2 + p_sum[1] ** 2)

        x1[i] = lorentz_dot(p_target, p_sum) / lorentz_dot(p_target, p_cms)
        x2[i] = lorentz_dot(p_beam, p_sum) / lorentz_dot(p_beam, p_cms)

        costheta[i] = 2.0 * (p_neg[3] * p_pos[2] - p_pos[3] * p_neg[2]) / mass[i] / np.sqrt(mass[i] * mass[i] + pT[i] * pT[i])

        phi[i] = np.arctan2(
            2.0 * np.sqrt(mass[i] * mass[i] + pT[i] * pT[i]) * (p_neg[0] * p_pos[1] - p_pos[0] * p_neg[1]),
            mass[i] * (p_pos[0] * p_pos[0] - p_neg[0] * p_neg[0] + p_pos[1] * p_pos[1] - p_neg[1] * p_neg[1])
        )
        sintheta[i] = np.sqrt(1 - costheta[i] ** 2)
        p_sum = boost(p_sum, -bv_cms)
        xF[i] = 2.0 * p_sum[2] / np.sqrt(s) / (1.0 - mass[i] * mass[i] / s)
    
    return mass, pT, x1, x2, xF, costheta, sintheta, phi

class Calc:
    def __init__(self):
        self.mom = None
    
    def calculate(self, mom):
        self.mom = mom
        return calcVariables(self.mom)

# Create an instance of dataOrganizer
organizer = DataOrganizer()

# Call the organizeData() method to populate the necessary attributes
organizer.organizeData()

# Get the mom array
mom = organizer.grab_mom()

# Ensure mom has the shape (N, 6)
print("Shape of mom:", mom.shape)

# Create an instance of Calc
calculator = Calc()

# Pass the correct mom array to calcVariables
mass, pT, x1, x2, xF, costheta, sintheta, phi = calculator.calculate(mom)

# Print the results
print("Mass:", mass)
print("pT:", pT)
print("x1:", x1)
print("x2:", x2)
print("xF:", xF)
print("Costheta:", costheta)
print("Sintheta:", sintheta)
print("Phi:", phi)