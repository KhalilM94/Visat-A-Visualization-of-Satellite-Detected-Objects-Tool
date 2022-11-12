import rasterio

def writeImage(m,t,c,outname,outFormat="GTiff",Resampled=1):
    """
    Generate sigmaNoughtdB rasters in GeoTiff and PNG formats .
    ----------
    Parameters
    ----------
    m,t,c,outname,outFormat="GTiff",Resampled=1
    footprint : list
    Dicionaries of all the object tiles existing in the JSON file
    ax : matplotlib.axes._subplots.AxesSubplot
    """
    dsFactor = 1/6

    if outFormat=="GTiff" and Resampled==1:
        outFile = "outGTiff/"+ outname + "_sigmaNoughtdB_Resampled" + ".tif"
    elif outFormat=="PNG" and Resampled==1:
        outFile = "outPNG/"+ outname + "_sigmaNoughtdB_Resampled" + ".png"
    elif outFormat=="GTiff" and Resampled==0:
        outFile = "outGTiff/"+ outname + "_sigmaNoughtdB" + ".tif"
        dsFactor = 1
    
    rastTransform = rasterio.Affine(t.a * dsFactor, t.b, t.c, t.d, t.e * dsFactor, t.f)
    rastHeight = int(m.shape[0] * dsFactor)                   
    rastWidth = int(m.shape[1] * dsFactor)

    if outFormat== "GTiff":
        RasterOut = rasterio.open(
            outFile, "w", 
            driver = outFormat,
            height = rastHeight,
            width = rastWidth,
            count = 1,
            nodata = -9999,
            dtype = m.dtype,
            crs = c,
            transform = rastTransform)
    elif outFormat== "PNG" :
        RasterOut = rasterio.open(
            outFile, "w", 
            driver = outFormat,
            height = rastHeight,
            width = rastWidth,
            count = 1,
            nodata = -9999,
            dtype = m.dtype,
            transform = rastTransform)

    RasterOut.write(m, 1)
    RasterOut.close()
    return 0