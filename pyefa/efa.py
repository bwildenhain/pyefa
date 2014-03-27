#!/usr/bin/env python
# -*- coding: utf-8 -*-
import models
import datetime

#class EFA(triprequest.TripRequest):
#	debug = False
#	def __init__(self, **args):
#		pass
#			
#	def submit(self, url, post, outputtype):
#		post.update({'outputFormat': outputtype, 'coordOutputFormat': 'WGS84'})
#		if self.debug and os.path.isfile('cache.%s' % outputtype): return open('cache.%s' % outputtype, 'r').read()
#		response = urllib2.urlopen(url, urllib.urlencode(post)).read()
#		if self.debug: open('cache.%s' % outputtype, 'w').write(response)
#		return response


		
class Request(models.Request):
	def __init__(self):
		pass
	
class TripResult(models.TripResult):
	def __init__(self):
		pass
		
	def later(self):
		pass
		
	def earlier(self):
		pass

	@classfunction
	def load(self, form, to, via, ):

	

	
	
