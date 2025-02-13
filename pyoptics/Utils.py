import numpy as np
from math import factorial
def zernike_radial(n, m, r):
    R = np.zeros_like(r)
    for k in range((n - m) // 2 + 1):
        num = (-1) ** k * factorial(n - k)
        denom = factorial(k) * factorial((n + m) // 2 - k) * factorial((n - m) // 2 - k)
        R += num / denom * r ** (n - 2 * k)
    return R

def zernike_polynomial(n, m, r, theta):
    if m > 0:
        return zernike_radial(n, m, r) * np.cos(m * theta)
    elif m < 0:
        return zernike_radial(n, -m, r) * np.sin(-m * theta)
    else:
        return zernike_radial(n, 0, r)


def generate_phase(size =256 ,n=1,m=1):

    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    X, Y = np.meshgrid(x, y)
    r = np.sqrt(X ** 2 + Y ** 2)
    theta = np.arctan2(Y, X)

    phase = np.zeros_like(r)

    Z = np.zeros_like(r)
    mask = r <= 2
    Z[mask] = zernike_polynomial(n, m, r[mask], theta[mask])
    phase=Z
    while np.min(phase)<0:
        phase[phase<0] = phase[phase<0]+2*np.pi

    while np.max(phase)>2*np.pi:
        phase[phase>2*np.pi] = phase[phase>2*np.pi]-2*np.pi

    return phase



def generate_random_phase(size=256, num_order=4):

    n_m_list=[]

    num_terms = round(num_order*(num_order+1)/2)
    for n in range(0,20 + 1):
        for m in range(-n, n + 1):
            if n % 2 == abs(m) % 2:  # 确保 m 和 n 的奇偶性一致
                n_m_list.append((n, m))

    coefficients = np.random.uniform(-5, 5, size=num_terms)

    # for i in range(num_terms):
    #     if i >20:
    #         coefficients[i]=coefficients[i] * 5

    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    X, Y = np.meshgrid(x, y)
    r = np.sqrt(X ** 2 + Y ** 2)
    theta = np.arctan2(Y, X)

    phase = np.zeros_like(r)

    for i in range(num_terms):
        n, m = n_m_list[i+1]
        Z = np.zeros_like(r)
        mask = r <= 2
        Z[mask] = zernike_polynomial(n, m, r[mask], theta[mask])
        phase += coefficients[i] * Z

    while np.min(phase)<0:
        phase[phase<0] = phase[phase<0]+2*np.pi

    while np.max(phase)>2*np.pi:
        phase[phase>2*np.pi] = phase[phase>2*np.pi]-2*np.pi

    return phase