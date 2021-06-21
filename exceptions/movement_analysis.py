#                                   #
#----------3D Biomechanics----------#
#                                   #
class ShapeDataFrame3DError(Exception):
    def __init__(self, message='DataFrame has not the appropriate number of columns. \nShould be four.'):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}'

class ColNamesDataFrame3DError(Exception):
    def __init__(self, message='DataFrame has not the appropriate names of columns. \nShould contain 0: time, 1: joint_x, 2: joint_y, 3: joint_z'):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}'

#                                   #
#----------2D Biomechanics----------#
#                                   #
class ShapeDataFrame2DError(Exception):
    def __init__(self, message='DataFrame has not the appropriate number of columns. \nShould be three.'):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}'

class ColNamesDataFrame2DError(Exception):
    def __init__(self, message='DataFrame has not the appropriate names of columns. \nShould contain 0: time, 1: joint_x, 2: joint_y'):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}'

#                            #
#----------Analysis----------#
#                            #
class LengthArraysError(Exception):
    def __init__(self, message='Arrays of x, y, z coordinates do not have the same length.'):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}'

class FpsError(Exception):
    def __init__(self, message='Fps value is invalid.'):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}'