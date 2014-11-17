#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import pandas as pd
from procrustes import procrustes
import matplotlib.pyplot as plt
import cv2
import numpy as np

"""
This module has all the classes and methods for setting up 
the training data (coordinates and images)
"""


class DataTrain(object):
	"""
	Class for contain dataframe with coordinates and 
	image information
	"""
	def __init__(self, filename_xy, path_images, nrows=None, ids=False):
		self.filename = filename_xy
		self.path_images = path_images
		self.data = self.load_data(ids, nrows)

	def load_data(self, ids=False, nrows=None):
		df = pd.read_csv(self.filename, sep=",", nrows=nrows)
		if not ids:
			df.drop(['tag'], inplace=True, axis=1)
		#df.sort(axis=1, inplace=True)

		return df

#TODO convert this to test

def main(filename_xy, path_images):
	my_data = DataTrain(filename_xy, path_images, ids=True)
	print my_data.data['tag'][1]
	
if __name__ == '__main__':
	main("data/use.txt", "images/")