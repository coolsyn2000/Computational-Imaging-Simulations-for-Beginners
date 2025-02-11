import pyoptics
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


def main():
    sourceLayer = pyoptics.GaussianBeamLayer(L=512 * 1e-6, N=512, wavelength=532e-9, radius=15e-6)
    lensLayer = pyoptics.LensLayer(L=512 * 1e-6, N=512, wavelength=532e-9, focal_length=5e-3)
    apertureLayer = pyoptics.ApertureLayer(L=512 * 1e-6, N=512, wavelength=532e-9, radius=100e-6)
    lensLayer2 = pyoptics.LensLayer(L=512 * 1e-6, N=512, wavelength=532e-9, focal_length=5e-3)

    Layers_list = [sourceLayer, lensLayer, apertureLayer, lensLayer2]
    Distance_list = [5e-3, 5e-3, 5e-3, 5e-3]

    four_f_system = pyoptics.OpticsSystem(Layers_list, Distance_list)
    z = 20e-3
    # z(m): propagation distance along Z axis
    z_step = 1e-4
    # z_step: simulation step of Z axis

    # simulation of light filed propagation along Z axis
    number_of_z_step = int(z / z_step)

    field_along_z = four_f_system.field_propagation_along_z(z, z_step)
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
                   np.abs(sourceLayer.field) ** 2, cmap='seismic')
    ax2.set_xlabel('X-axis (μm)')
    ax2.set_ylabel('Y-axis (μm)')
    ax2.set_title('Initial field amplitude')

    ax3 = fig.add_subplot(gs[1, 1])
    ax3.pcolormesh(sourceLayer.X * 10 ** 6, sourceLayer.Y * 10 ** 6,
                   np.abs(four_f_system.field_propagation(z)), cmap='seismic')
    ax3.set_xlabel('X-axis (μm)')
    ax3.set_ylabel('Y-axis (μm)')
    ax3.set_title('Final field amplitude')

    plt.tight_layout()
    #plt.savefig('./assets/4f_system_simulation.png')
    plt.show()



if __name__ == "__main__":
    main()
