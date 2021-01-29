import random


class cube:
    def __init__(self, start_x, start_y, start_z, step_x, step_y, step_z, step_amount_x, step_amount_y, step_amount_z):
        #those are the boundaries for our cube
        self.start_x = start_x
        self.start_y = start_y
        self.start_z = start_z
        self.step_x = step_x
        self.step_y = step_y
        self.step_z = step_z
        self.step_amount_x = step_amount_x
        self.step_amount_y = step_amount_y
        self.step_amount_z = step_amount_z
        self.x_axis = []
        self.y_axis = []
        self.z_axis = []
        self.axis_init(start_x,step_x,step_amount_x, self.x_axis)
        self.axis_init(start_y, step_y, step_amount_y, self.y_axis)
        self.axis_init(start_z, step_z, step_amount_z, self.z_axis)





    def axis_init(self ,start, step_size, step_amount, axis):
        for i in range(0, step_amount):
            axis.append(start + i * step_size)


    def random_plain_accessess(self ,axis_a, axis_b):
        pairings = []
        for i in range(0, len(axis_a)):
            for j in range(0, len(axis_b)):
                pairing = (axis_a[i], axis_b[j])
                pairings.append(pairing)
        random.shuffle(pairings)
        print 'length plain pairings'
        print len(pairings)
        return pairings

    def random_bottom_up_y_axis_accesses(self):

        pairings = []
        for i in range(0, len(self.y_axis)):
            y_coordinate = self.y_axis[i]

            plain_pairings = self.random_plain_accessess(self.x_axis, self.z_axis)
            for j in range(0, len(plain_pairings)):
                x_coordinate = plain_pairings[j][0]
                z_coordinate = plain_pairings[j][1]
                pairing = (x_coordinate,y_coordinate,z_coordinate)
                pairings.append(pairing)

        return pairings


    def random_bottom_up_y_axis_accesses_with_pause(self):

        pairings = []
        coordinates = []
        for i in range(0, len(self.y_axis)):
            y_coordinate = self.y_axis[i]

            plain_pairings = self.random_plain_accessess(self.x_axis, self.z_axis)
            for j in range(0, len(plain_pairings)):
                x_coordinate = plain_pairings[j][0]
                z_coordinate = plain_pairings[j][1]
                pairing = (x_coordinate,y_coordinate,z_coordinate)
                pairings.append(pairing)

        return pairings




