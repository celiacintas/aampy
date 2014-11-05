#!/usr/bin/env python2
# -*- coding: utf-8 -*-

""" 
Module for (after) generalize any haarcascade classiffier
"""

import os
import sys
from os.path import basename, splitext
import cv2
from cv2 import cv
import argparse


class Finder(object):
    """docstring for Finder"""
    def __init__(self, path_cascade):
        """Load the images and the haarcascade files"""
        super(Finder, self).__init__()
        self.cascade = cv2.CascadeClassifier(path_cascade)

    def get_roi(self, img):
        """Get the ROI of each image with the parameters finded in paper EARS"""
        rects = self.cascade.detectMultiScale(img, 1.2, 3, 0
                                            |cv.CV_HAAR_FIND_BIGGEST_OBJECT
                                            |cv.CV_HAAR_DO_ROUGH_SEARCH
                                            |cv.CV_HAAR_SCALE_IMAGE,
                                            (0, 0))

        if len(rects) == 0:
            return []
        rects[:, 2:] += rects[:, :2]

        return rects

def draw_rectangles(img, rects):
    """Draw rectangle of ROI"""
    for x_1, y_1, x_2, y_2 in rects:
        cv2.rectangle(img, (x_1, y_1), (x_2, y_2), (127, 255, 0), 2)

    return img


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
                                     'Iris Segmentation')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--file", dest="file", default=None,
                        help='Pass the path of the file to be process')
    group.add_argument("--folder", dest="folder", default=None,
                        help='Pass the path of the file to be process')
    args = parser.parse_args()

    if args.file:
        filename = [args.file]
    elif args.folder:
        filename = map(lambda f: os.path.join(args.folder, f),
                        os.listdir(args.folder))
    else:
        parser.print_help()
        sys.exit(1)

    IMAGES = [cv2.imread(path, 0) for path in filename]
    my_finder = Finder("haarcascades/haarcascade_mcs_leftear.xml")
    for i, image in enumerate(IMAGES):
        rect = my_finder.get_roi(image)
        draw_rectangles(image, rect)
        cv2.imwrite('/tmp/out{}.jpg'.format(splitext(basename(filename[i]))[0]),
                                            image)
