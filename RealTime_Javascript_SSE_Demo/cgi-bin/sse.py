#!/usr/bin/env python

import random
import sys

lat = 25.042185 + 0.002*(random.random()-0.5)
lon = 121.614548 + 0.002*(random.random()-0.5)

sys.stdout.write('Content-type: text/event-stream \r\n\r\n')

sys.stdout.write('data: {"lat":%s, "lon":%s} \r\n' % (lat,lon))
sys.stdout.write('retry: 5000\r\n\r\n')
sys.stdout.flush()