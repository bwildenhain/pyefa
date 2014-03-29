#!/usr/bin/env python3
import datetime, requests

class API:
	debug = True
	def __init__(self):
		pass
		
	def __repr__(self):
		return '%s()' % self.__class__.__name__
		
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
		self.dataTime  = datetime.datetime.now()
		self.interface = None
		self.url       = None
		self.post      = None
		
		self.sessionID     = None
		self.requestID     = None
		self.serverID      = None
		self.serverVersion = None
		self.clientIP      = None
		self.clientAgent   = None
		
		self.result = None
		
class Location:
	def __init__(self):
		self.x = None
		self.y = None
	
class City:
	def __init__(self, name=None):
		self.id = None
		self.name = name
		
	def __repr__(self):
		return 'City(%s #%s)' % (repr(self.name), repr(self.id))
	
class Stop(Location):
	def __init__(self, city=None, name=None):
		self.id = None
		self.name = name
		self.city = City(city) if isinstance(city, str) else city
		
	def __repr__(self):
		return 'Stop(%s, %s #%s)' % (repr(self.city), repr(self.name), repr(self.id))
		
class Address(Location):
	def __init__(self, city=None, name=None):
		self.name = name
		self.city = City(city) if isinstance(city, str) else city
		self.street = None
		self.number = None
		
	def __repr__(self):
		return 'Address(%s, %s #%s)' % (repr(self.city), repr(self.name), repr(self.id))
		
class OdvUnclear(Location):
	def __init__(self, reason=None, possibilities=[]):
		self.reason = reason
		self.possibilities = possibilities
		
	def __repr__(self):
		return 'OdvUnclear(%s, %s)' % (repr(self.reason), repr(self.possibilities))
		
class TripResult(Request):
	def __init__(self):
		self.origin      = None
		self.destination = None
		self.via         = []
		
		self.time = None
		self.timetype = None
		self.exclude = None
		self.include = None
		self.max_interchanges      = None
		self.select_interchange_by = None
		self.use_near_stops        = None
		self.walk_speed   = None
		self.with_bike    = None
		self.use_realtime = None
		
		self.trips = []
		
	def earlier(self):
		self.api.earlier(self)
		
	def later(self):
		self.api.later(self)
		
class Trip():
	def __init__(self):
		self.network = None
		self.vehicle_time    = None
		self.public_duration = None
		self.parts           = []
		self.next_departures = []
		
		self.ticket_adult = None
		self.ticket_child = None
		self.ticket_bike_adult = None
		self.ticket_bike_child = None
		self.special_tickets = []
		
class TicketType():
	def __init__(self, name=None, authority=None, adult=None, child=None):
		self.name = name
		self.authority = authority
		self.category  = None
		
		self.adult = adult
		self.child = child
		
class Ticket():
	def __init__(self, category=None, price=None, currency=None):
		self.id = None
		self.price    = price
		self.currency = currency
		self.category = category
		
class TripPart():
	def __init__(self):
		self.origin      = None
		self.destination = None
		self.locations   = []
		
		self.mot       = None
		self.text      = None
		
		
