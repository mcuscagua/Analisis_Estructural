def distribuida_total(w,L):
    return (w * L**3) / 24

def distribuida_parcial(w,L,s):
    alpha1 = w * s**2 * (2 * L - s)**2 / (24 * L)
    alpha2 = w * s ** 2 * (2 * L**2 - s**2) / (24 * L)
    return alpha1, alpha2

def puntual(P, a, b, L):
    alpha1 = P * a * b * (b + L) / (6 * L)
    alpha2 = P * a * b * (a + L) / (6 * L)
    return alpha1, alpha2

def distribuida_media(w,s,L):
    return w * s * (3 * L ** 2 - s ** 2) / 48

def triangular_total(w,L):
    alpha1 = w * L ** 3 / 45
    alpha2 = 7 * w * L ** 3 / 360
    return  alpha1, alpha2

def momento(M,L,a,b):
    alpha1 = M * (L / 6) * (3 * b ** 2 / L ** 2 - 1)
    alpha2 = M * (L / 6) * (1 - 3 * a ** 2 / L ** 2)
    return alpha1, alpha2

def piram_total(w,L):
    return 5 * w * L ** 3 /192

def piram_media(w,s,L):
    return w * s * (3 * L ** 2 - 2 * s ** 2) / 48

def dos_triang_juntas(w,L):
    return w * L ** 3 / 64

def dos_triang_separa(w,s,L):
    return w * s ** 2 * (2 * L - s) / 24

def trapesoidal(w,L,a):
    return w * (L ** 3 - a ** 2 * (2 * L - a)) / 24