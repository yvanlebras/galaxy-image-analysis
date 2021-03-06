import argparse
import sys
import pandas as pd
import skimage.io
from skimage.measure import label
from skimage.data import checkerboard
import numpy as np



def binaryimage2points(input_file):
    img_in = skimage.io.imread(input_file) 
    
    #make label image
    label = skimage.measure.label(img_in)
    
    #amount of regions
    amount_label = np.max(label)
    
    # iterate over all regions in order to calc center of mass
    center_mass = []
    for i in range(1,amount_label+1):    
        #get coordinates of region
        coord = np.where(label==i)
        # be carefull with x,y coordinates
        center_mass.append([np.mean(coord[1]),np.mean(coord[0])])

    #make data frame of detections
    out_dataFrame = pd.DataFrame(center_mass)


    #return
    return(out_dataFrame)

    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='input file')
    parser.add_argument('out_file', help='out file (CSV)')
    
    args        = parser.parse_args()
    input_file  = args.input_file
    out_file    = args.out_file
    
    #TOOL
    out_dataFrame = binaryimage2points(input_file)
    
    #Print to csv file
    out_dataFrame.to_csv(out_file,index=False,header=False)
