import numpy as np


class OpticsLayer:
    def __init__(self, L, N, wavelength):
        self.L = L
        self.N = N
        self.x, self.y, self.X, self.Y = self.gen_mesh_grid()
        self.dx = L / N
        self.initial_field = np.zeros((N, N)).astype(np.complex64)
        self.field = np.zeros((N, N)).astype(np.complex64)
        self.wavelength = wavelength

    def gen_mesh_grid(self):
        x = np.linspace(-self.L / 2, self.L / 2, self.N)
        y = np.linspace(-self.L / 2, self.L / 2, self.N)
        X, Y = np.meshgrid(x, y)
        return x, y, X, Y

    def init_field(self):
        """
        simulate initial complex field。
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def modulated_field(self, modulation_list):
        if self.field.shape != modulation_list[0].shape:
            raise ValueError(f"field-array shape do not match: {self.field.shape} 和 {modulation_list[0].shape}")
        self.field = self.initial_field

        for i in range(len(modulation_list)):
            self.field = self.field * modulation_list[i]

    def angular_propagation(self, distance):
        U0_fft = np.fft.fftshift(np.fft.fft2(self.field))
        fx = np.fft.fftshift(np.fft.fftfreq(self.N, self.dx))
        fy = np.fft.fftshift(np.fft.fftfreq(self.N, self.dx))
        Fx, Fy = np.meshgrid(fx, fy)
        k = 2 * np.pi / self.wavelength
        H = np.exp(1j * k * distance * np.sqrt(1 - (self.wavelength * Fx) ** 2 - (self.wavelength * Fy) ** 2))
        Uz_fft = U0_fft * H
        Uz = np.fft.ifft2(np.fft.ifftshift(Uz_fft))

        return Uz

    def angular_propagation_along_z(self, distance, number_of_steps):
        z_ind = np.arange(0, number_of_steps)
        z_step = distance / number_of_steps
        z = z_ind * z_step
        propagation_field_along_z = np.zeros((len(z_ind), 512, 512), dtype=np.complex64)
        propagation_field_along_z[0] = np.abs(self.field)

        for ind in z_ind[1:]:
            ind = int(ind)
            propagation_field_along_z[int(ind)] = self.angular_propagation(distance=z[ind])

        return propagation_field_along_z


class LensLayer(OpticsLayer):
    def __init__(self, L, N, wavelength, focal_length):
        super().__init__(L, N, wavelength)
        self.focal_length = focal_length  # 焦距
        self.init_field()

    def init_field(self):
        self.initial_field = np.exp(-1j * np.pi / (self.wavelength * self.focal_length) * (self.X ** 2 + self.Y ** 2))
        self.field= self.initial_field

class GaussianBeamLayer(OpticsLayer):
    def __init__(self, L, N, wavelength, radius, angleX=0, angleY=0):
        super().__init__(L, N, wavelength)
        self.radius = radius
        self.angleX= angleX
        self.angleY= angleY
        self.init_field()
        #self.modulated_field([np.ones((N, N), dtype=np.complex64)])

    def init_field(self):

        k = 2 * np.pi / self.wavelength  # 波数

        # 根据入射角计算相位
        phase = k * (self.X * np.sin(self.angleX) + self.Y * np.sin(self.angleY))

        self.initial_field = np.exp(-(self.X ** 2 + self.Y ** 2) / self.radius ** 2) * np.exp(1j * phase)

        self.field = self.initial_field


class ApertureLayer(OpticsLayer):
    def __init__(self, L, N, wavelength, radius):
        super().__init__(L, N, wavelength)
        self.radius = radius
        self.init_field()

    def init_field(self):
        self.initial_field[np.sqrt(self.X ** 2 + self.Y ** 2) <= self.radius] = 1
        self.initial_field[np.sqrt(self.X ** 2 + self.Y ** 2) > self.radius] = 0
        self.field = self.initial_field


class ObjectLayer(OpticsLayer):
    def __init__(self, L, N, wavelength, mag=None, pha=None):
        super().__init__(L, N, wavelength)
        self.mag, self.pha = mag, pha
        self.init_field()
        self.modulated_field([np.ones((N, N), dtype=np.complex64)])

    def init_field(self):

        if self.mag is None:
            self.mag = np.ones((self.N, self.N))
        elif self.field.shape != self.mag.shape:
            raise ValueError(f"field-array shape do not match: {self.field.shape} 和 {self.mag.shape}")

        if self.pha is None:
            self.pha = np.zeros((self.N, self.N))
        elif self.field.shape != self.pha.shape:
            raise ValueError(f"field-array shape do not match: {self.field.shape} 和 {self.pha.shape}")

        self.initial_field = self.mag * np.exp(1j * self.pha)
        self.field = self.initial_field


class RefractionLayer(OpticsLayer):
    def __init__(self, L, N, wavelength, angleX=0, angleY=0):
        super().__init__(L, N, wavelength)
        self.angleX = angleX
        self.angleY = angleY
        self.init_field()

    def init_field(self):
        k = 2 * np.pi / self.wavelength
        phase = k * (self.X * np.sin(self.angleX) + self.Y * np.sin(self.angleY))
        self.initial_field = np.exp(1j * phase)
        self.field = self.initial_field
