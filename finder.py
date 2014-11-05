#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import cv2
from cv2 import cv
import numpy as np
import argparse
import os
from os.path import basename, splitext


class Finder(object):
    """docstring for Finder"""
    def __init__(self, path_cascade):
        """Load the images and the haarcascade files"""
        super(Finder, self).__init__()
        self.cascade = cv2.CascadeClassifier(path_cascade)
    

    def get_roi(self, image):
        """Get the ROI of each image with the parameters finded in paper EARS"""
        rects = self.cascade.detectMultiScale(image, 1.2, 3, 0 |cv.CV_HAAR_FIND_BIGGEST_OBJECT |cv.CV_HAAR_DO_ROUGH_SEARCH
                                  |cv.CV_HAAR_SCALE_IMAGE, (0, 0))
        
        if len(rects) == 0:
            return []
        rects[:, 2:] += rects[:, :2]
        
        return rects

    def draw_rectangles(self, image, rects):
        """Draw rectangle of ROI"""
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(image, (x1, y1), (x2, y2), (127, 255, 0), 2)

        return image    


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
        filename = map(lambda f: os.path.join(args.folder, f), os.listdir(args.folder))
    else:
        parser.print_help()
        sys.exit(1)

    images = [cv2.imread(path, 0) for path in filename]
    my_finder = Finder("haarcascades/haarcascade_mcs_leftear.xml")
    for i, image in enumerate(images):
        rect = my_finder.get_roi(image)
        my_finder.draw_rectangles(image, rect)
        cv2.imwrite('/tmp/lero_{}.jpg'.format(splitext(basename(filename[i]))[0]), image)
