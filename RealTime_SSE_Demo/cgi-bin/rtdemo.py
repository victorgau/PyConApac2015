#!/usr/bin/env python

from rtdemo.rtdemo import Map

rt = Map("http://localhost:8000/cgi-bin/sse.py")
rt._build_map()

print "Content-Type: text/html"
print
print rt.HTML
