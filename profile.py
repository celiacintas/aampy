#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
from os.path import splitext, basename, join
from aampy.finder import Finder, NoROIException
from aampy.data import DataTrain
from aampy.vector_profile import VectorProfile1D, VectorProfile2D

# this has to be in some draw-tools .. #TODO locate better later
def draw_landmarks(image, coordinates):
    """
    Draw the landmarks in the image
    """
    for coord in coordinates: #2D coordinates
        cv2.circle(image, (int(coord[0]), int(coord[1])), 5, (200, 200, 200), -1)

    return image

def draw_whisker(image, whiskers):
    """
    Draw the whiskers ...
    """
    list_whiskers = whiskers.values()[0]
    for w in range(len(list_whiskers)-1):
        v = list_whiskers[w].vector.astype(np.int)
        cv2.line(image, (v[0], v[1]), (v[0] + v[2], v[1] + v[3]), (255, 20, 20))

# this has to be in some blabla-tools .. #TODO locate better later
def get_roi_coordinates(coordinates, rect):
    """
    Translate the general coordinates to the ROI rect
    """
    return map(lambda c: [coordinates[c] - rect[0], coordinates[c + 1] - rect[1]], 
               range(0, len(coordinates), 2))


class Profile(object):
    """docstring for Profile"""
    def __init__(self, filename_xy, path_images, haarcascade):
        super(Profile, self).__init__()
        self.data_train = DataTrain(filename_xy, path_images)
        self.finder = Finder(haarcascade)
        self.vectors = {}
        # move this to a numpy array/ dataframe pandas for faster work

    def load_vectors(self, id_people, vectors_type):
        """
        Take the ortogonal vectors for 1D and 9 cell neigh for 2D profiles.
        """
        tmp_vec = []
        #FIX the vector should be anato sig, not only the next node

        for n in range(len(vectors_type)-1): #nasty fix
            if vectors_type[n] == '1D':
                tmp_vec.append(VectorProfile1D(self.coordinates[n: n + 2], self.magnitude))
            elif vectors_type[n] == '2D':
                self.vectors.append(VectorProfile2D(self.coordinates[n: n + 2], self.magnitude))

        self.vectors[id_people] = tmp_vec
        
        return self.vectors

    def load_profile(self):
        """
        for each individual we search the vector 1D or 2D profile with magnitudes of sobel
        images around the landmarks.
        """
        
        for image_id in self.data_train.get_ids():
            image_filename = [filename for filename in os.listdir( self.data_train.path_images) if filename.startswith(image_id)]
            try:
                image = cv2.imread(join(self.data_train.path_images, image_filename[0]), 0)
                tmp_rect = self.finder.get_roi(image)
                self.magnitude, real_rect = self.finder.preprocess_image(image, tmp_rect)
            except NoROIException, e:
                print e
            except IndexError, e:
                print e, "Image File Not Found" #TODO create exc
            else:    
                self.coordinates = get_roi_coordinates(self.data_train.get_landmarks(image_id, image.shape), real_rect)
                #print self.coordinates, len(self.coordinates)
                whiskers_tmp = self.load_vectors(image_id, ['1D'] * 4) # FIX this should be in datatrain class
                #print whiskers_tmp
                #TODO only for debug remove later or build flag option
                mag_tmp = draw_landmarks(self.magnitude, self.coordinates[:4*2])
                #mag_tmp = draw_whisker(self.magnitude, whiskers_tmp)
                cv2.imwrite('/tmp/out{}.jpg'.format(splitext(basename(image_filename[0]))[0]),
                                                mag_tmp)
            

#TODO this are nasty tests
def main(filename_xy, path_images, haarcascade):
    my_profile = Profile(filename_xy, path_images, haarcascade)
    my_profile.load_profile()

if __name__ == '__main__':
    package_directory = os.path.dirname(os.path.abspath(__file__))
    main(join(package_directory, "data/use.txt"), join(package_directory,"tmp/images/"), 
         join(package_directory, "haarcascades/haarcascade_mcs_leftear.xml"))