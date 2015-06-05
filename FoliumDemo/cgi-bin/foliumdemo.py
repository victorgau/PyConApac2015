#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import folium

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
    center=(25.0410877,121.6113313)
    markers = generateMarkers(center=center, n=5)

    map = folium.Map(location=center, zoom_start=18)
    for marker in markers:
        map.simple_marker([marker[0], marker[1]], popup=str(marker))
    map._build_map()

    print "Content-Type: text/html"
    print
    print map.HTML

if __name__=="__main__":
    main()