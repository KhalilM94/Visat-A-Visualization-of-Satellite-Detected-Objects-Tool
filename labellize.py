#!/usr/bin/python
import os
import sys
import warnings
import rasterio
import numpy as np
import geopandas as gpd
import glob
import json
from rasterio.mask import mask
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import resources

class Tile():
    """
    Creates the Object Tile plot 
    """
    def __init__(self, footprint, ax):
        """
        Parameters
        ----------
        footprint : list
        Dicionaries of all the object tiles existing in the JSON file
        ax : matplotlib.axes._subplots.AxesSubplot
        """
        self.footprint = footprint
        self.ind = 0
        self.ax = ax
    def on_press(self, event):
        if event.key == ' ' or event.key == 'enter':
            if self.ind < len(self.footprint):
                self.ax.set_visible("True")
                img = self.ax.imshow(self.footprint[self.ind]["Object Tile"][0])
                plt.title(self.footprint[self.ind]["Label"])
                plt.draw()
                self.ind += 1
            else:
                plt.close()
                sys.exit(0)


def labellize():
    args = sys.argv
    if len(args) != 4:
        print("Usage : labellize.py [Image Id] [Data folder] [JSON file of labels]")
        sys.exit()
    else:
        dataPath = args[2]+"/ICEYE_X*_GRD_*_"+args[1]+"_*.tif"
        dataList = glob.glob(dataPath)

        if dataList == []:
            print("No image with ID "+ args[1] + " was found!")
            sys.exit()
        
        try:
            labelsFile = open(args[3])
        except OSError:
                print("Could not open/read file:", labelsFile)
                sys.exit()
        
        try:
            labels= json.load(labelsFile)
        except Exception as e:
            print("Exception: %s" % str(e))
            sys.exit()

        warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        
        for imagePath in dataList:
            image = imagePath.split('/')[2]
            imageName = image.split('.')[0]
            try:
                rastFile = rasterio.open(imagePath)
            except rasterio.errors.RasterioIOError:
                print("Error opening ",image)
                continue
            rasterArray = rastFile.read()[0]
            cf = float(rastFile.tags()['CALIBRATION_FACTOR'])

            norm = np.linalg.norm(rasterArray)
            normalArray = rasterArray/norm

            sigmaNought = np.dot(cf,np.square(np.abs(normalArray)))
            sigmaNoughtdB = np.float32(np.dot(10,np.log10(sigmaNought)))
            sigmaNoughtdB16 = sigmaNoughtdB.astype(np.uint16)

            if not os.path.exists("outPNG"):
                os.mkdir("outPNG")
                    
            if not os.path.exists("outGTiff"):
                os.mkdir("outGTiff")
            
            resources.writeImage(sigmaNoughtdB16,rastFile.transform,rastFile.crs,imageName,"PNG",1)
            resources.writeImage(sigmaNoughtdB,rastFile.transform,rastFile.crs,imageName,"GTiff",1)
            resources.writeImage(sigmaNoughtdB,rastFile.transform,rastFile.crs,imageName,"GTiff",0)
                
            rastFile.close()
        
        snGTIFF = "./outGTiff/*.tif"
        snList = glob.glob(snGTIFF)

        features = []
        for imagePath in snList:
            backScatter = rasterio.open(imagePath)
            features.extend(resources.getFeatures(labels,backScatter))
            backScatter.close()

        gdf = gpd.GeoDataFrame.from_features(features)

  
        footprint = []
        for imagePath in snList:
            backScatter = rasterio.open(imagePath)
            #print(backScatter.name, " opened")
            features.extend(resources.getFeatures(labels,backScatter))
            for item in gdf.index:
                object = gdf.iloc[item]
                if object["External ID"] == imagePath.split('/')[2].strip("_sigmaNoughtdB.tif"):
                    objectTiles = resources.getObjectTiles(object,backScatter)
                    footprint.append(objectTiles)
            backScatter.close()
        
        """
        Display the sequence of object tiles with their respective labels, 
        and navigate to the next object tile when pressing space or enter,
        until all have been shown.
        """
        
        fig, ax = plt.subplots()
        ax.axis("off")
        plt.title("Pess Enter or Space bar to start navigating")
        callback = Tile(footprint,ax)

        fig.canvas.mpl_connect('key_press_event', callback.on_press)
        plt.show()


if __name__ == "__main__":
    labellize()