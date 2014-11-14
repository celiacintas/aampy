#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import pandas as pd
from procrustes import procrustes
import matplotlib.pyplot as plt



class DataTest(object):
	def __init__(self, filename, nrows=None, ids=False):
		self.filename = filename
		self.data = self.load_data(ids, nrows)

	def load_data(self, ids=False, nrows=None):
		df = pd.read_csv(self.filename, sep=",", nrows=nrows)
		if not ids:
			df.drop(['tag'], inplace=True, axis=1)
		#df.sort(axis=1, inplace=True)

		return df

	def preprocess_image(self):


#TODO convert this to test

def main(filename):
	my_shapes = []
	my_data = DataTest(filename, ids=True)
	print my_data.data['tag'][0]
	
if __name__ == '__main__':
	main("data/use.txt")