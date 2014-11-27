#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np

# this can be 1 or 2D
class VectorProfile(object):
	"""docstring for VectorProfile"""
	def __init__(self, arg):
		super(VectorProfile, self).__init__()
		self.arg = arg

class VectorProfile1D(VectorProfile):
	"""docstring for VectorProfile1D"""
	def __init__(self, coordinate, image_mag):
		super(VectorProfile1D, self).__init__()
		self.vector = self.__get_perpendicular(coordinate, image_mag)
	
	def __get_perpendicular_norm(self, coordinates_vector, image_mag):
		vector_a = np.array(coordinates_vector)
		vector_perp = np.empty_like(vector_a)
		vector_perp[0] = -vector_a[1]
		vector_perp[1] = vector_a[0]
		#a/np.linalg.norm(a)
		#after this get the mag values in the directrion of vect and norm

class VectorProfile2D(VectorProfile):
	"""docstring for VectorProfile2D"""
	def __init__(self, arg):
		super(VectorProfile2D, self).__init__()
		self.arg = arg

	def get_neigh():
		pass