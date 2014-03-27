#!/usr/bin/env python
import datetime, requests

class API:
	debug = True
	def __init__(self):
		pass
		
	def tripRequest(self, origin, destination, via=None, datetime=None,
					timetype='dep', exclude=('ice', 'ic'), max_interchanges=9,
					select_interchange_by='speed', use_near_stops=False,
					walk_speed='normal', with_bike=False, use_realtime=True):		
		pass
		
	def earlier(self):
		pass
		
	def later(self):
		pass
		
	def submit(self, url, post):
		r = requests.post(url, data=post)
		#if self.debug and os.path.isfile('cache.%s' % outputtype): return open('cache.%s' % outputtype, 'r').read()
		response = r.text
		if self.debug: open('cache.xml', 'w').write(response)
		return response

class Request:
	def __init__(self):
		self.time      = datetime.datetime.now()
		self.interface = None
		self.url       = None
		self.post      = None
		
		self.sessionID     = None
		self.requestID     = None
		self.serverID      = None
		self.serverVersion = None
		self.clientIP      = None
		
class Location():
	pass
	
class City():
	def __init__(self, name=None):
		self.id = None
		self.name = name
	
class Stop(Location):
	def __init__(self, city=None, name=None):
		self.id = None
		self.name = name
		self.city = City(city) if isinstance(city, str) else city
		
class TripResult():
	def __init__(self, api):
		self.api = api
		
		self.origin      = None
		self.destination = None
		self.via         = None
		
		self.request = []
		pass
		
	def earlier(self):
		self.api.earlier(self)
		
	def later(self):
		self.api.later(self)
