#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
from data_test import DataTest
from procrustes import procrustes


ORIGIN_X = ORIGIN_Y = 0.

class Shape(object):
		def __init__(self, landmarks, name):
			self.xy = np.array(landmarks, dtype=np.int)
			self.nr_landmarks =  self.xy.shape[0]/2
			self.name = name
			self.centroid = self.get_centroid()
		
		def load_shape(self, shape):
			pass

		def translate_shape(self, direction):
		
			T = np.identity(3)
			T[:2, 2] = direction[:2]

			return T

		def get_centroid(self):
			centroid = self.xy.mean(0)
			
			return centroid

		def align_shape(self, mean_shape):
			"""
			Procrustes fit
			"""
			n, m = mean_shape.xy.shape
			ny, my = self.xy.shape
			reflection = 'best'
			scaling = True

			X0 = mean_shape.xy - mean_shape.centroid
			Y0 = self.xy - self.centroid

			ssX = (X0**2.).sum()
			ssY = (Y0**2.).sum()

		    # centred Frobenius norm
			normX = np.sqrt(ssX)
			normY = np.sqrt(ssY)

			# scale to equal (unit) norm
			X0 /= normX
			Y0 /= normY

			if my < m:
			    Y0 = np.concatenate((Y0, np.zeros(n, m-my)),0)

		    # optimum rotation matrix of Y
			A = np.dot(X0.T, Y0)
			U,s,Vt = np.linalg.svd(A,full_matrices=False)
			V = Vt.T
			T = np.dot(V, U.T)

			if reflection is not 'best':

		        # does the current solution use a reflection?
				have_reflection = np.linalg.det(T) < 0

		        # if that's not what was specified, force another reflection
				if reflection != have_reflection:
					V[:,-1] *= -1
					s[-1] *= -1
					T = np.dot(V, U.T)

			traceTA = s.sum()

			if scaling:

				# optimum scaling of Y
				b = traceTA * normX / normY

				# standarised distance between X and b*Y*T + c
				d = 1 - traceTA**2

				# transformed coords
				Z = normX*traceTA*np.dot(Y0, T) + mean_shape.centroid

			else:
				b = 1
				d = 1 + ssY/ssX - 2 * traceTA * normY / normX
				Z = normY*np.dot(Y0, T) + mean_shape.centroid

			# transformation matrix
			if my < m:
				T = T[:my,:]
			c = mean_shape.centroid - b*np.dot(self.centroid, T)

		    #transformation values 
			tform = {'rotation':T, 'scale':b, 'translation':c}

			self.xy = Z.copy()
			print d

		def plot_shape(self):
			return plt.plot(self.xy[:,0], self.xy[:,1], 'o')


def main(filename):
	my_shapes = []
	my_data = DataTest(filename, 200, ids=False)

	for row in my_data.data.iterrows():
		my_shapes.append(Shape(row[1][:].reshape(45, 2),'lero'))
	for shape in my_shapes:
		shape.align_shape(my_shapes[0])
	
	for shape in my_shapes:
		shape.plot_shape()
	plt.axis('equal')
	plt.show()

if __name__ == '__main__':
	main("data/use.txt")