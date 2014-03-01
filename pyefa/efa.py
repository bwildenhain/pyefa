#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib, urllib2
import os, json
import triprequest

class EFA(triprequest.TripRequest):
	debug = False
	def __init__(self, **args):
		pass
			
	def submit(self, url, post, outputtype):
		post.update({'outputFormat': outputtype, 'coordOutputFormat': 'WGS84'})
		if self.debug and os.path.isfile('cache.%s' % outputtype): return open('cache.%s' % outputtype, 'r').read()
		response = urllib2.urlopen(url, urllib.urlencode(post)).read()
		if self.debug: open('cache.%s' % outputtype, 'w').write(response)
		return response
		
#EFA().submit()

	
	
