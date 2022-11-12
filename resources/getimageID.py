from argparse import ArgumentParser

def getimageID(imageName):
    """
    Extracts the <IMAGE_ID> from the filename  
    """
    return imageName.split('_')[4]

if __name__ == "__main__":
    
    parser=ArgumentParser(description="getImageID")
    parser.add_argument('-name', type=str,default='',help="Filename Name of patter ICEYE_X<number>_GRD_<SM/SL>_<IMAGE-ID>_<timestamp>.tif")
    args = parser.parse_args()
    getimageID(args.name)