def get_ObjectRange(xObject):
    
    xObjectxMin = xObject.get_xMin()
    xObjectyMin = xObject.get_yMin()
    xObjectxMax = xObject.get_xMax()
    xObjectyMax = xObject.get_yMax()
    
    xObjectRange = (xObjectxMax - xObjectxMin) * (xObjectyMax - xObjectyMin)
    
    return xObjectRange