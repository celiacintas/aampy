#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import pandas as pd


"""
This module has all the classes and methods for setting up 
the training data (coordinates and images)
"""


class DataTrain(object):
	"""
	Class for contain dataframe with coordinates and 
	image information
	"""
	def __init__(self, filename_xy, path_images, nrows=None, ids=True):
		self.filename = filename_xy
		self.path_images = path_images
		self.data = self.load_data(ids, nrows)

	def load_data(self, ids=False, nrows=None):
		df = pd.read_csv(self.filename, index_col='tag', nrows=nrows)
		# should add a column to say if the landmarks has to have 1D or 2D profiles?
		#df.sort(axis=1, inplace=True)

		return df

	def get_ids(self):
		"""
		Return ids of the samples to search images or get landmarks
		"""
		return list(self.data.index.values)

	def get_landmarks(self, id_people, fullsize):
		"""
		Return the landmarks of some particular id, and change de origin
		location tps diffs opencv
		"""
		landmarks = self.data.loc[[id_people]].values[0]
		for coord in range(1, len(landmarks), 2): #only y-values
			landmarks[coord] = fullsize[0] - landmarks[coord]

		return landmarks

#TODO convert this to test

def main(filename_xy, path_images):
	my_data = DataTrain(filename_xy, path_images, ids=True)
	
if __name__ == '__main__':
	package_directory = os.path.dirname(os.path.abspath(__file__))
	main(os.path.join(package_directory, "data/use.txt"), os.path.join(package_directory,"images/"))