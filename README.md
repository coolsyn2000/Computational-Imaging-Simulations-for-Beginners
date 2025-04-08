# Pyoptics
A simple and easy-modified python library for optical diffraction simulation 

define optical path with `class OpticsLayer` and build system with `class OpticsSystem`

## Usage
Build optical system with custom layer and set distances among the layers
```
import pyoptics

# Build Layers and System
sourceLayer = pyoptics.GaussianBeamLayer(L=512 * 1e-6, N=512, wavelength=532e-9, radius=15e-6)
lensLayer = pyoptics.LensLayer(L=512 * 1e-6, N=512, wavelength=532e-9, focal_length=5e-3)

Layers_list = [[sourceLayer], [lensLayer]]
Distance_list = [5e-3, 5e-3]

four_f_system = pyoptics.OpticsSystem(Layers_list, Distance_list)
```

Simulate wave propagation within single line code
```
z = sum(Distance_list) #z(m): propagation distance along Z axis
z_step = 1e-4 #z_step: simulation step of Z axis
number_of_z_step = int(z / z_step)

# simulation of light filed propagation along Z axis
field_along_z = four_f_system.field_propagation_along_z(z, z_step)

# wave propagtion at depth of Z
field_at_z = four_f_system.field_propagation(z)
```


## Example
There are several examples in "./examples", which are presented in Jupyter Notebooks with code and markdown clearly.
01. Gaussian beam propagation in 4f system
02. Memory effect scattering speckle


