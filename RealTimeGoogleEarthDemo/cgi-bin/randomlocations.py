#!/usr/bin/env python
 
import random
 
latitude = 25.042185 + 0.002*(random.random()-0.5)
longitude = 121.614548 + 0.002*(random.random()-0.5)
kml = """<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Placemark>
    <name>(%f, %f)</name>
    <LookAt>
    <longitude>%f</longitude>
    <latitude>%f</latitude>
        <altitude>0</altitude>
    <range>100</range>
    <tilt>30</tilt>
    <heading>0</heading>
        <altitudeMode>relativeToGround</altitudeMode> 
    </LookAt>
    <Point>
    <coordinates>%f,%f,%f</coordinates>
    </Point>
    </Placemark>
    </kml>""" % (latitude, longitude, longitude, latitude, longitude, latitude, 0)
print 'Content-Type: application/vnd.google-earth.kml+xml\n'
print kml