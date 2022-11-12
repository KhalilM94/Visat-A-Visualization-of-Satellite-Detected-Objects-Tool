def getFeatures(labels,raster):
    """
    Reformat the JSON file to GeoJSON structure 
    and transform the polygons coordinates to match raster extent.
    """
    features = []
    featureId = 0

    heightPNG = 4096
    widthPNG = 2815
    heightGRD = raster.height
    widthGRD = raster.width

    for image in labels:
        imID = image["External ID"]
        if raster.name.split('/')[2].split('.')[0].strip("_sigmaNoughtdB") == imID.split('.')[0]:
            for label in image:
                if label == 'Label' and isinstance(image[label],str)==0:
                    for prop in image[label]:
                        for geometryList in image[label][prop]:
                            for geometry in geometryList:
                                xlist = []
                                ylist = []
                                for coordinates in geometryList[geometry]:
                                    xlist.append(coordinates["x"]*widthGRD//widthPNG)
                                    ylist.append(coordinates["y"]*heightGRD//heightPNG)
                                polygon = list(c for c in zip(xlist, ylist))
                                feature = { "type": "Feature", "properties": { "id": int(featureId), "External ID": imID.split('.')[0] , "Label": prop }, 
                                           "geometry": { "type": "Polygon", "coordinates": [polygon]}}
                                featureId += 1
                                features.append(feature)
    return features