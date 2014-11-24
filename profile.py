#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import cv2
from os.path import splitext, basename, join
from aampy.finder import Finder, NoROIException
from aampy.data import DataTrain
from aampy.tmp.nasty_tools import draw_landmarks

class Profile(object):
	"""docstring for Profile"""
	def __init__(self, filename_xy, path_images, haarcascade):
		super(Profile, self).__init__()
		self.data_train = DataTrain(filename_xy, path_images)
		self.finder = Finder(haarcascade)
		self.vectors = []
		# move this to a numpy array for faster work

	def load_profile(self):
		
		for image_id in self.data_train.get_ids():
			image_filename = [filename for filename in os.listdir( self.data_train.path_images) if filename.startswith(image_id)]
			try:
				print image_filename[0]
				image = cv2.imread(join(self.data_train.path_images, image_filename[0]), 0)
				rect = self.finder.get_roi(image)
				mag = self.finder.preprocess_image(image, rect)
				draw_landmarks(mag, self.data_train.get_landmarks(image_id), image.shape)
				cv2.imwrite('/tmp/out{}.jpg'.format(splitext(basename(image_filename[0]))[0]),
				                                mag)
			except NoROIException, e:
			    print e
			except IndexError, e:
				print e, "Image File Not Found"

# this can be 1 or 2D
class VectorProfile(object):
	"""docstring for VectorProfile"""
	def __init__(self, arg):
		super(VectorProfile, self).__init__()
		self.arg = arg


# this are nasty tests
def main(filename_xy, path_images, haarcascade):
	my_profile = Profile(filename_xy, path_images, haarcascade)
	my_profile.load_profile()

if __name__ == '__main__':
	package_directory = os.path.dirname(os.path.abspath(__file__))
	main(join(package_directory, "data/use.txt"), join(package_directory,"images/"), 
		 join(package_directory, "haarcascades/haarcascade_mcs_leftear.xml"))