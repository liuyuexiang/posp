def convertToDegree(RawDegrees):
    RawDegrees = int(RawDegrees,16)
    RawAsFloat = float(RawDegrees/1000000)
    # firstdigits = int(RawDegrees/100000) 
    # nexttwodigits = RawAsFloat - float(firstdigits*100000) 
    
    # Converted = float(firstdigits + nexttwodigits/60.0)
    # Converted = '{0:.6f}'.format(Converted) 
    return str(RawAsFloat)

lat = convertToDegree('015eac32')
print(lat)
lng = convertToDegree('06c1c6f8')
print(lng)