import pyoptics
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import imageio

def main():
    np.random.seed(888)
    random_pha = np.angle(np.fft.fft2(np.random.rand(512, 512)))
    sourceLayer = pyoptics.GaussianBeamLayer(L=512 * 1e-6, N=512, wavelength=532e-9, radius=100e-6, angleX=0,
                                             angleY=0)
    aperture = pyoptics.ApertureLayer(L=512 * 1e-6, N=512, wavelength=532e-9, radius=15e-6)
    scatter = pyoptics.ObjectLayer(L=512 * 1e-6, N=512, wavelength=532e-9, pha=random_pha)
    angleX_ind = np.linspace(-0.02, 0.02, 21)
    filenames=[]

    for i in range(len(angleX_ind)):

        refractiveLayer = pyoptics.RefractionLayer(L=512 * 1e-6, N=512, wavelength=532e-9, angleX=angleX_ind[i], angleY=0)

        Layers_list = [[sourceLayer, refractiveLayer, scatter, aperture]]
        Distance_list = [7e-4]

        OMEsystem = pyoptics.OpticsSystem(Layers_list, Distance_list)
        z = sum(Distance_list)
        # z(m): propagation distance along Z axis
        z_step = 1e-5
        # z_step: simulation step of Z axis

        # simulation of light filed propagation along Z axis
        number_of_z_step = round(z / z_step)

        field_along_z = OMEsystem.field_propagation_along_z(z, z_step)
        YZ_field = np.abs(field_along_z[:, 512 // 2])
        z_total = np.arange(0, number_of_z_step) * z_step

        fig = plt.figure(figsize=(10, 12))
        gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])  # 2行2列的网格

        ax1 = fig.add_subplot(gs[0, :])
        ax1.pcolormesh(z_total * 10 ** 3, sourceLayer.x * 10 ** 6, YZ_field.T, cmap='seismic')
        ax1.set_xlabel('Propagation Distance (mm)')
        ax1.set_ylabel('Spatial Coordinate (μm)')
        ax1.set_title('Field amplitude along Z-axis')

        ax2 = fig.add_subplot(gs[1, 0])
        ax2.pcolormesh(sourceLayer.X * 10 ** 6, sourceLayer.Y * 10 ** 6,
                       np.abs(OMEsystem.field_propagation(z)), cmap='seismic')
        ax2.set_xlabel('X-axis (μm)')
        ax2.set_ylabel('Y-axis (μm)')
        ax2.set_title('Final field amplitude')

        ax3 = fig.add_subplot(gs[1, 1])
        ax3.plot(sourceLayer.x * 10 ** 6, np.abs(OMEsystem.field_propagation(z))[512//2,:])
        ax3.set_xlabel('X-axis (μm)')
        ax3.set_ylabel('Amplitude')
        ax3.set_title('Field along line')
        plt.tight_layout()

        plt.savefig('OME_system_%.3fRad.png' % (angleX_ind[i]))
        filenames.append('OME_system_%.3fRad.png' % (angleX_ind[i]))
        plt.show()

    with imageio.get_writer('./assets/angular_ome_simulation.gif', mode='I', duration=0.2) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
        for filename in reversed(filenames):
            image = imageio.imread(filename)
            writer.append_data(image)

    import os
    for filename in filenames:
        os.remove(filename)

if __name__ == "__main__":
    main()
