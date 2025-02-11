from .Layers import *


class OpticsSystem:
    def __init__(self, Layers, Distances):
        if not isinstance(Layers, list) or not isinstance(Distances, list):
            raise TypeError("inputs must be list")
        if len(Layers) != len(Distances):
            raise ValueError("Layers and Distance should have same length")
        self.Layers = Layers
        self.Distances = Distances

    def field_propagation_along_z(self, z, z_step):

        new_distance_list = []
        current_sum = 0
        for distance in self.Distances:
            current_sum += distance
            if current_sum < z:
                new_distance_list.append(distance)
            elif current_sum >= z:
                new_distance_list.append(z - (current_sum - distance))
                break
        new_distance_list = [num for num in new_distance_list if num != 0]

        number_of_z_steps = round(new_distance_list[0] / z_step)
        field_along_z_total = self.Layers[0].angular_propagation_along_z(distance=new_distance_list[0],
                                                                         number_of_steps=number_of_z_steps)

        for index in range(1, len(new_distance_list)):
            self.Layers[index].modulated_field(field_along_z_total[-1])
            number_of_z_steps = round(new_distance_list[index] / z_step)
            field_along_z_single = self.Layers[index].angular_propagation_along_z(distance=new_distance_list[index],
                                                                                  number_of_steps=number_of_z_steps)
            field_along_z_total = np.concatenate((field_along_z_total, field_along_z_single), axis=0)

        return field_along_z_total

    def field_propagation(self, z):

        # remove the layers which are out of range
        new_distance_list = []
        current_sum = 0
        for distance in self.Distances:
            current_sum += distance
            if current_sum < z:
                new_distance_list.append(distance)
            elif current_sum >= z:
                new_distance_list.append(z - (current_sum - distance))
                break
        new_distance_list = [num for num in new_distance_list if num != 0]

        field = self.Layers[0].angular_propagation(distance=new_distance_list[0])

        for index in range(1, len(new_distance_list)):
            self.Layers[index].modulated_field(field)

            field = self.Layers[index].angular_propagation(distance=new_distance_list[index])

        return field
