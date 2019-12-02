def dist_total(w,L):
    return (w * L**3) / 24

def dist_parcial(w,L,s):
    alpha1 = w * s**2 * (2 * L - s)**2 / (24 * L)
    alpha2 = w * s ** 2 * (2 * L**2 - s**2) / (24 * L)
    return alpha1, alpha2

def puntual(P, a, b, L):
    alpha1 = P * a * b * (b + L) / (6 * L)
    alpha2 = P * a * b * (a + L) / (6 * L)
    return alpha1, alpha2