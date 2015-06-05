#!/usr/bin/env python

from jinja2 import Environment, PackageLoader

ENV = Environment(loader=PackageLoader('rtdemo', 'templates'))

class Map(object):
    def __init__(self, ssescript):
        self.ssescript = ssescript
        self.env = ENV

    def _build_map(self):
        # get template
        html_templ = self.env.get_template("realtimetracking.html")

        # render template
        self.HTML = html_templ.render(ssescript=self.ssescript)