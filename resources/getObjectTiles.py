from rasterio.mask import mask

def getObjectTiles(item, raster):
    """
    Returns a numPy 2D array that represents the cropped object tile.
    """
    iterable = []
    dic = {}
    iterable.append(item["geometry"])
    objectTile = mask(raster, iterable, crop=True, nodata=-9999)
    dic["imageID"] = item["External ID"]
    dic["Label"] = item["Label"]
    dic["Object Tile"] = objectTile[0]
    return dic