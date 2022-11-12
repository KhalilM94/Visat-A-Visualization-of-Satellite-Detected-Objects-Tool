from datetime import datetime
from argparse import ArgumentParser

def getTimestamp(imageName):
    """
    Extracts the <timestamp> from the filename in RFC3339 format  
    """
    timeStamp = imageName.split('_')[5].split('.')[0]
    return datetime.strptime(timeStamp, '%Y%m%dT%H%M%S').isoformat()

if __name__ == "__main__":
    
    parser=ArgumentParser(description="getTimestamp")
    parser.add_argument('-name', type=str,default='',help="Filename Name of patter ICEYE_X<number>_GRD_<SM/SL>_<IMAGE-ID>_<timestamp>.tif")
    args = parser.parse_args()
    getTimestamp(args.name)