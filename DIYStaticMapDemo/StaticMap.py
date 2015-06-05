#!/usr/bin/env python

from PIL import Image
import math
import requests
from StringIO import StringIO
import random
import geocoder

class StaticMap:
    def __init__(self, width=640, height=480, center=(25.042185, 121.614548), zoom=14):
        self.width = width
        self.height = height
        self.zoom = zoom
        self.center = center
        self.Cxy = self.deg2xy(center, zoom, False)
        self.Txy = self.deg2xy(center, zoom)
        self.mapImage =  Image.new("RGB", (width, height), "black")
        self.centerImage = Image.open("purpleflag.png")
        self.markerImage = Image.open("push_pin.png")

    def createBaseMap(self):
        x0 = self.width / 2.0
        y0 = self.height / 2.0

        tx = self.Txy[0]
        ty = self.Txy[1]

        xr = self.Cxy[0] % 256
        yr = self.Cxy[1] % 256

        tl = int((x0-xr)/256.0)+1
        tr = int((self.width-(x0-xr))/256.0)+1

        tu = int((y0-yr)/256.0)+1
        td = int((self.height-(y0-yr))/256.0)+1    

        i = 0
        x = tx - tl

        while i < tl + tr:
            j = 0
            y = ty - tu
            while j < td + tu:
                #imgurl = "http://{a}.tile.openstreetmap.org/{z}/{x}/{y}.png".format(a='a',z=self.zoom,x=x+i, y=y+j)
                #imgurl = "http://otile1.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg".format(z=self.zoom,x=x+i, y=y+j)
                #imgurl = "http://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}".format(z=self.zoom,x=x+i, y=y+j)
                imgurl = "http://tile.stamen.com/terrain/{z}/{x}/{y}.jpg".format(z=self.zoom,x=x+i, y=y+j)
                r = requests.get(imgurl)
                im = Image.open(StringIO(r.content))
    
                self.mapImage.paste(im,(int(x0-xr) - tl*256 + i*256,int(y0-yr) - tu*256 + j*256))
                j = j + 1
            i = i + 1

    def deg2xy(self, deg, zoom, isTile=True):
        """deg=(lat,lon)"""
        lat_rad = math.radians(deg[0])
        n = 2.0 ** zoom if isTile else 2.0 ** zoom * 256.0
        x = int((deg[1] + 180.0) / 360.0 * n)
        y = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return (x, y)

    def xy2deg(self, xy, zoom, isTile=True):
        """xy=(x,y)"""
        n = 2.0 ** zoom if isTile else 2.0 ** zoom * 256.0
        lon_deg = xy[0] / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * xy[1] / n)))
        lat_deg = math.degrees(lat_rad)
        return (lat_deg, lon_deg)

    def addMarker(self, deg):
        """deg=(lat,lon)"""
        markerxy = self.deg2xy(deg, self.zoom, False)
        Xnw = self.Cxy[0]-self.width/2
        Ynw = self.Cxy[1]-self.height/2
        x = markerxy[0] - Xnw
        y = markerxy[1] - Ynw
        if (x >=0 and x<self.width) and (y>=0 and y<self.height):
            w = self.markerImage.size[0]
            h = self.markerImage.size[1]
            self.mapImage.paste(self.markerImage, (x-w/2,y-h),self.markerImage)

    def addCenter(self):
        W = self.width
        H = self.height
        w = self.centerImage.size[0]
        h = self.centerImage.size[1]
        self.mapImage.paste(self.centerImage, ((W-w)/2,H/2-h),self.centerImage)

    def saveMap(self, imageName):
        self.mapImage.save(imageName,"PNG")

def generateMarkers(center=(25.042185, 121.614548), n=5):
    c = 0
    markers = []
    while c < n:
        latitude = center[0] + 0.002*(random.random()-0.5)
        longitude = center[1] + 0.002*(random.random()-0.5)
        markers.append((latitude,longitude))
        c = c + 1
    return markers

def main():
    #center=(25.0410877,121.6113313)
    center=geocoder.osm("New York City").latlng
    map = StaticMap(center=center, width=800, height=600, zoom=15)
    map.createBaseMap()
    map.addCenter()

    markers = generateMarkers(center=center)
    for marker in markers:
        map.addMarker(marker)

    map.saveMap("test00.png")

if __name__=="__main__":
    main()
