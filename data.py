#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import pandas as pd
from procrustes import procrustes
import matplotlib.pyplot as plt



class DataTrain(object):
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

	def preprocess_image(self, image_id):
		prefixed = [filename for filename in os.listdir( self.path_images) if filename.startswith(image_id)]
		print prefixed

#TODO convert this to test

def main(filename_xy, path_images):
	my_shapes = []
	my_data = DataTrain(filename_xy, path_images, ids=True)
	name = my_data.data['tag'][1]
	print name
	my_data.preprocess_image(name)
	#print my_data.data['tag'][0]
	
if __name__ == '__main__':
	main("data/use.txt", "images/")