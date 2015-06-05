#!/usr/bin/env python

import random
 
def generateMarkers(n=5):
    c = 0
    markers = []
    while c < n:
        latitude = 25.042185 + 0.002*(random.random()-0.5)
        longitude = 121.614548 + 0.002*(random.random()-0.5)
        markers.append((latitude,longitude))
        c = c + 1
    return markers
 
def centerOfMarkers(markers):
    lat = 0.0
    lon = 0.0
 
    for marker in markers:
        lat = lat + marker[0]
        lon = lon + marker[1]
 
    lat = lat / float(len(markers))
    lon = lon / float(len(markers))
 
    return (lat, lon)
 
def getBaseMap(center, zoom=16, width=640, height=480):
    url = "http://maps.google.com/maps/api/staticmap?center=%s,%s&zoom=%d&size=%dx%d" % \
    (center[0],center[1],zoom,width,height)
    return url
 
def addMarkers(markers):
    strMarkers = ""
    i = 0
    for marker in markers:
        strMarkers += "&markers=label:" + str(i) + "|" + str(marker[0]) + "," + str(marker[1])
        i = i + 1
    return strMarkers
 
def addPath(markers, color='0xff0000ff', weight=5):
    strPath = "&path=color:%s|weight:%d" % (color, weight)
    for marker in markers:
        strPath += "|"+str(marker[0])+","+str(marker[1])
    return strPath
 
def addSensorStat(sensor=False):
    if sensor:
        return "&sensor=true"
    else:
        return "&sensor=false"
 
def main():
    markers = generateMarkers(5)
    center = centerOfMarkers(markers)
    url = getBaseMap(center,zoom=18) + addMarkers(markers) + addPath(markers)  + addSensorStat()
    #url = getBaseMap(center, zoom=18) + addMarkers(markers)

    print "Content-Type: text/html"
    print
    print '<img src="%s" />' % url 
 
if __name__=="__main__":
    main()