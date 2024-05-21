from numpy import array, dot

def lorentz_dot_product(lorentz_vector_a, lorentz_vector_b):
    """
    This does pa.pb. The order is important:
    column_pa times [Matrix] times column_pb.
    """
    minkownski_metric = array([[1., 0., 0., 0.], [0., -1., 0., 0.], [0., 0., -1., 0.], [0., 0., 0., -1.]])
    # Lorentzian metric signature (+, -, -, -)

    four_vector_product = dot(lorentz_vector_a, minkownski_metric.dot(lorentz_vector_b))

    return four_vector_product

def calculate_invariant_mass(four_momentum_particle_one, four_momentum_particle_two):
    """
    Calculates the invariant mass.
    """

    lorentz_dot_product(four_momentum_particle_one, four_momentum_particle_two)

    pass