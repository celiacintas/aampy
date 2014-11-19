#!/usr/bin/env python2
# -*- coding: utf-8 -*-

""" 
Module for (after) generalize any haarcascade classiffier
"""

import os
import sys
import cv2
from cv2 import cv
import argparse
import numpy as np
from os.path import basename, splitext


class NoROIException(Exception):
    """Exception for no ROI finded"""

    def __init__(self):
        Exception.__init__(self, "ROI not found")


class Finder(object):
    """docstring for Finder"""
    def __init__(self, path_cascade):
        """Load the images and the haarcascade files"""
        super(Finder, self).__init__()
        self.cascade = cv2.CascadeClassifier(path_cascade)

    def get_roi(self, img): #1.2, 3 , 0
        """Get the ROI of each image with the parameters finded in paper EARS"""
        rects = self.cascade.detectMultiScale(img, 1.05, 3, 0
                                            |cv.CV_HAAR_FIND_BIGGEST_OBJECT
                                            |cv.CV_HAAR_DO_ROUGH_SEARCH
                                            |cv.CV_HAAR_SCALE_IMAGE,
                                            (0, 0))
        try:
            if len(rects) == 0:
                raise NoROIException()
        except NoROIException, e:
            raise NoROIException()
        else:
            rects[:, 2:] += rects[:, :2]
            print rects
            return rects[0]

    def preprocess_image(self, img, rect):
        """"""
        offset = 50
        # x_1, y_1, x_2, y_2  rect
        tmp = img[rect[1] - offset :rect[3] + offset, rect[0] - offset: rect[2] + offset]
        norm = cv2.normalize(tmp, tmp, 0, 255, cv2.NORM_MINMAX , cv2.CV_8UC1)
        print norm
        grad_y = cv2.Sobel(norm, cv2.CV_32F, 0, 1, ksize=3)
        grad_x = cv2.Sobel(norm, cv2.CV_32F, 1, 0, ksize=3)
        mag = cv2.magnitude(grad_x, grad_y)
        print np.max(mag), mag.argmax(axis=0)
        return mag

def draw_rectangles(img, rects):
    """Draw rectangle of ROI"""
    for x_1, y_1, x_2, y_2 in rects:
        cv2.rectangle(img, (x_1, y_1), (x_2, y_2), (127, 255, 0), 2)

    return img


if __name__ == '__main__':


    parser = argparse.ArgumentParser(description=
                                     'ROI extraction of ears (for now)')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--file", dest="file", default=None,
                        help='Pass the path of the file to be process')
    group.add_argument("--folder", dest="folder", default=None,
                        help='Pass the path of the file to be process')
    args = parser.parse_args()

    if args.file:
        filenames = [args.file]
    elif args.folder:
        filenames = map(lambda f: os.path.join(args.folder, f),
                        os.listdir(args.folder))
    else:
        parser.print_help()
        sys.exit(1)

   
    #IMAGES = [cv2.imread(path, 0) for path in filename]
    # this was nice but kill the mem
    my_finder = Finder("haarcascades/haarcascade_mcs_leftear.xml")
    for file in filenames:
        print file
        image = cv2.imread(file, 0)
        try:
            rect = my_finder.get_roi(image)
            mag = my_finder.preprocess_image(image, rect)
            cv2.imwrite('/tmp/out{}.jpg'.format(splitext(basename(file))[0]),
                                            mag)
        except NoROIException, e:
            print e
            
        #draw_rectangles(image, rect)
        
