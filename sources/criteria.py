import numpy as np 
from numpy.polynomial.polynomial import polyfit

def angle(vector_1, vector_2):
    # Returns the angle in radians between two vectors of equal dimension
    
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)
    
    return angle


def fitting_error(x, y):
    # Normalization
    max_x = np.max(x)
    max_y = np.max(y)
    min_x = np.min(x)
    min_y = np.min(y)
    
    if (max_x == min_x):
        x = np.zeros((len(x)))
    else :
        x = (x - min_x) / (max_x - min_x)
        
    if (max_y == min_y):
        y = np.zeros((len(y)))
    else :
        y = (y - min_y) / (max_y - min_y)
            
    results = polyfit(x, y, 1, full= True)
    b = results[0][0]
    a = results[0][1] 
    
    residuals = results[1][0]                                                       # Sum of squared residuals of the least squares fit
    fitting_error = residuals/len(x)
    return a, b, fitting_error
    