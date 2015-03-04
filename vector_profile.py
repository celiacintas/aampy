#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np

# this can be 1 or 2D
class VectorProfile(object):
    """docstring for VectorProfile"""
    def __init__(self, coordinate, image):
        super(VectorProfile, self).__init__()
        self.coordinate = coordinate
        self.image = image

class VectorProfile1D(VectorProfile):
    """docstring for VectorProfile1D"""
    def __init__(self, coordinate, image_mag):
        super(VectorProfile1D, self).__init__(coordinate, image_mag)
        self.vector = self.__get_perpendicular_norm(coordinate)
        # this is tmp
        #self.vector = self.__get_pixels_vector(tmp_vector, image_mag)
    
    def __get_perpendicular_norm(self, coordinates_vector):
        """
        """
        vector_a = np.array(coordinates_vector).flatten()
        # Get the direction vector going from A to B.
        # vector_a [x1, y1, x2, y2]
        print vector_a, vector_a.shape
        vector_move = (vector_a[2] - vector_a[0], vector_a[3] - vector_a[1])
        # Normalize the vector
        mag_vector = np.sqrt(vector_move[0] * vector_move[0] + vector_move[1] * vector_move[1])
        norm_vector = (vector_move[0] / mag_vector, vector_move[1] / mag_vector)
        #In OpenCV it's the opposite. So, for example to get clockwise rotation in OpenCV: 
        temp_vector = (-norm_vector[1], norm_vector[0])
        #Create a new line at B pointing in the direction of v:  
        #C.x = B.x + v.x * length; C.y = B.y + v.y * length;
        #(Note that you can make it extend in both directions by creating a point 
        #D in the opposite direction by simply negating length.)
        output_vec = (vector_a[0] + temp_vector[0] * 2, vector_a[1] + temp_vector[1] * 2)
        #vector_perp = np.empty_like(vector_a)
        #vector_perp[0] = -vector_a[1]
        #vector_perp[1] = vector_a[0]

        return np.array([(vector_a[0], vector_a[1]),output_vec]).flatten()
        
    def __get_pixels_vector(self, vector, magnitude):
        """
        """
        #a/np.linalg.norm(a)
        #after this get the mag values in the directrion of vect and norm

class VectorProfile2D(VectorProfile):
    """docstring for VectorProfile2D"""
    def __init__(self, arg):
        super(VectorProfile2D, self).__init__()
        self.arg = arg

    def get_neigh():
        pass