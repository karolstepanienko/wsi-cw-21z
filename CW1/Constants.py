# Autor: Karol Stepanienko

class Constants:
    def __init__(self):
        # EPSILON Determines the precision of finding the minumum
        # Determines the precision of finding the minumum
        self.EPSILON_GRADIENT = pow(10, -4)
        self.EPSILON_DISTANCE = pow(10, -7)
        self.MAX_ROTATIONS = 3000


        # Starting points
        # For single variable function g
        self.X_START = 20
        self.SINGLE_ALFA = 0.003  # Determines the step size
    
        # Analytically calculated minimum
        self.X_IDEAL_POINT = 0


        # For function of two variables f
        self.X1_START = 0.2
        self.X2_START = -3
        self.X1X2_START = [self.X1_START, self.X2_START]
        self.DOUBLE_ALFA = 0.3

        # Analytically calculated minimum
        self.X1_IDEAL_POINT = 0
        self.X2_IDEAL_POINT = 0
        self.X1X2_IDEAL_POINTS = [self.X1_IDEAL_POINT, self.X2_IDEAL_POINT]
