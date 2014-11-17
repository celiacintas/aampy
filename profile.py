#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class Profile(object):
	"""docstring for Profile"""
	def __init__(self, arg):
		super(Profile, self).__init__()
		self.arg = arg

# this can be 1 or 2D
class VectorProfile(object):
	"""docstring for VectorProfile"""
	def __init__(self, arg):
		super(VectorProfile, self).__init__()
		self.arg = arg


#image_filename = [filename for filename in os.listdir( self.path_images) if filename.startswith(image_id)]
#        img = cv2.imread(os.path.join(self.path_images, image_filename[0]), 0)