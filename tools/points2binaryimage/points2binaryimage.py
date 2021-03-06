import argparse
import sys
import numpy as np
import skimage.io
import pandas as pd
import os
import warnings


def points2binaryimage(point_file, out_file, shape=[500, 500], has_header=False, invert_xy=False):

    img = np.zeros(shape, dtype=np.int16)
    if os.path.exists(point_file) and os.path.getsize(point_file) > 0:
        if has_header:
            df = pd.read_csv(point_file, skiprows=1, header=None)
        else:
            df = pd.read_csv(point_file, header=None)

        for i in range(0, len(df)):
            a_row = df.iloc[i]
            oob = False
            if int(a_row[0]) < 0 or int(a_row[1]) < 0:
                oob = True

            if invert_xy:
                if img.shape[0]<=int(a_row[0]) or img.shape[1]<=int(a_row[1]):
                    oob = True
                else:
                    img[int(a_row[0]), int(a_row[1])] = 32767
            else:
                if img.shape[0]<=int(a_row[1]) or img.shape[1]<=int(a_row[0]):
                    oob = True
                else:
                    img[int(a_row[1]), int(a_row[0])] = 32767
            if oob:
                print "[!] point %d:%d is out of image bounds %d:%d" % (int(a_row[0]), int(a_row[1]), shape[0], shape[1])
    else:
        print "[!] %s is empty or does not exist" % point_file

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        skimage.io.imsave(out_file, img)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('point_file', help='label file')
    parser.add_argument('out_file', help='out file (TIFF)')
    parser.add_argument('shapex', type=int, help='shapex')
    parser.add_argument('shapey', type=int, help='shapey')
    parser.add_argument('--has_header', dest='has_header', default=False, help='set True if CSV has header')
    parser.add_argument('--invert_xy', dest='invert_xy', default=False, help='invert x and y in CSV')

    args        = parser.parse_args()
    point_file  = args.point_file
    out_file    = args.out_file
    shapex      = args.shapex
    shapey      = args.shapey
    invert_xy   = args.invert_xy
    has_header  = args.has_header


    #TOOL
    points2binaryimage(point_file, out_file, [shapey, shapex], has_header=has_header, invert_xy=invert_xy)
