#!/usr/bin/env python

import cgi
from PIL import Image
import math
import requests
from StringIO import StringIO

def deg2xy(lat_deg, lon_deg, zoom, isTile=True):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom if isTile else 2.0 ** zoom * 256.0
    x = int((lon_deg + 180.0) / 360.0 * n)
    y = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (x, y)

def xy2deg(x, y, zoom, isTile=True):
    n = 2.0 ** zoom if isTile else 2.0 ** zoom * 256.0
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

def generateMarkers(lat=25.042185, lon=121.614548, n=5):
    c = 0
    markers = []
    while c < n:
        latitude = lat + 0.002*(random.random()-0.5)
        longitude = lon + 0.002*(random.random()-0.5)
        markers.append((latitude,longitude))
        c = c + 1
    return markers

def main():
    form = cgi.FieldStorage() 
 
    lat = float(form.getvalue('lat'))
    lon  = float(form.getvalue('lon'))
    zoom = int(form.getvalue('zoom'))
    width = int(form.getvalue('width'))
    height = int(form.getvalue('height'))

    x0 = width / 2.0
    y0 = height / 2.0

    Txy = deg2xy(lat, lon, zoom)
    Cxy = deg2xy(lat, lon, zoom, False)

    tx = Txy[0]
    ty = Txy[1]

    xr = Cxy[0] % 256
    yr = Cxy[1] % 256

    tl = int((x0-xr)/256.0)+1
    tr = int((width-(x0-xr))/256.0)+1

    tu = int((y0-yr)/256.0)+1
    td = int((height-(y0-yr))/256.0)+1    

    mapimg = Image.new("RGB", (width, height), "black")

    i = 0
    x = tx - tl

    while i < tl + tr:
        j = 0
        y = ty - tu
        while j < td + tu:
            imgurl = "http://{a}.tile.openstreetmap.org/{z}/{x}/{y}.png".format(a='a',z=zoom,x=x+i, y=y+j)
            r = requests.get(imgurl)
            im = Image.open(StringIO(r.content))
    
            mapimg.paste(im,(int(x0-xr) - tl*256 + i*256,int(y0-yr) - tu*256 + j*256))
            j = j + 1
        i = i + 1

    center = Image.open("cgi-bin/push_pin.png")
    mapimg.paste(center,(width/2-center.size[0]/2, height/2-center.size[1]),center)

    imgname = "test{w}x{h}.png".format(w=width,h=height)
    mapimg.save(imgname,"PNG")

    print "Content-Type: text/html"
    print
    print '<img src="/%s" />' % imgname

if __name__=="__main__":
    main()