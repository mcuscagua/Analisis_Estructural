# Puntual

def puntual(P, a, b, L):
    alpha1 = P * a * b * (b + L) / (6 * L)
    alpha2 = P * a * b * (a + L) / (6 * L)
    return alpha1, alpha2

# Distribuida

def distribuida_total(w,L):
    return (w * L**3) / 24

def distribuida_parcial(w,L,s):
    alpha1 = w * s**2 * (2 * L - s)**2 / (24 * L)
    alpha2 = w * s ** 2 * (2 * L**2 - s**2) / (24 * L)
    return alpha1, alpha2

def distribuida_media(w,s,L):
    return w * s * (3 * L ** 2 - s ** 2) / 48

# Triangular

def triangular_punt(P,s,L):
    alpha1 = P * s ** 2 * (40 * L ** 2 - 45 * s * L + 12 * s ** 2) / (360 * L)
    alpha2 = P * s ** 2 * (1 - (3 * s ** 2) / (5 * L ** 2)) / 18
    return alpha1, alpha2

def triangular_lado(P,s,L):
    alpha1 = P * s ** 2 * (20 * L ** 2  - 15 * s * L + 3 * s ** 2) / (360 * L)
    alpha2 = P * s ** 2 * L * (1 - (3 * s ** 2) / (10 * L ** 2)) / 36
    return alpha1, alpha2

def triangular_total(w,L):
    alpha1 = w * L ** 3 / 45
    alpha2 = 7 * w * L ** 3 / 360
    return alpha1, alpha2

def piram_total(w,L):
    return 5 * w * L ** 3 /192

def piram_media(w,s,L):
    return w * s * (3 * L ** 2 - 2 * s ** 2) / 48


# Momento

def momento(M,L,a,b):
    alpha1 = M * (L / 6) * (3 * b ** 2 / L ** 2 - 1)
    alpha2 = M * (L / 6) * (1 - 3 * a ** 2 / L ** 2)
    return alpha1, alpha2