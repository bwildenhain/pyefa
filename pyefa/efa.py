#!/usr/bin/env python3
import models
import datetime
from collections import Iterable
import xml.etree.ElementTree as ET

class API(models.API):
	url_triprequest = None
	mots = ('ice', 'ic', 'local', 's-bahn', 'u-bahn', 'stadtbahn', 'tram', 'stadtbus', 'regionalbus', 'schnellbus', 'seilbahn', 'schiff', 'ast', 'sonstige')
		
	def locationConverter(self, location):
		if location is None:
			return {'type': 'stop', 'place': '', 'name': ''}
		elif not isinstance(location, models.Location):
			return None
		elif isinstance(location, models.Stop):
			return {'type': location.name, 'place': location.city.name, 'name': location.name}
			
	def motsExcludeConverter(self, excludes):
		errors = set(excludes)-set(self.mots)
		if errors:
			print('Error')
			
		includes = set(self.mots)-set(excludes)
		
		if 'ice' in includes:
			if 'ic' not in includes or 'local' not in includes:
				print('Error')
			lineRestrictions = 400
		elif 'ic' in includes:
			if 'local' not in includes:
				print('Error')
			lineRestrictions = 401
		else:
			lineRestrictions = 403
		
		includes -= set(('ice', 'ic'))
		states = tuple(self.mots.index(mot)-2 for mot in includes)
		
		return states, lineRestrictions			
		
	def tripRequest(self, origin, destination, via=None, time=None,
					timetype='dep', exclude=('ice', 'ic'), max_interchanges=9,
					select_interchange_by='speed', use_near_stops=False,
					walk_speed='normal', with_bike=False, use_realtime=True):		
						
		now = datetime.datetime.now()
		
		# Parametervalidierung
		p_origin      = self.locationConverter(origin)
		p_destination = self.locationConverter(destination)
		p_via         = self.locationConverter(via)
		
		if time is not None and not isinstance(datetime, datetime.datetime):
			raise exceptions.SetupException('time', time, 'datetime.datetime')
		
		if timetype not in ['dep', 'arr']:
			raise exceptions.SetupException('timetype', timetype, '(dep|arr)')
			
		if not isinstance(exclude, Iterable):
			raise exceptions.SetupException('exclude', exclude, 'list with (%s)' % '|'.join(self.mots))
			
		if not isinstance(max_interchanges, int) or max_interchanges < 0:
			raise exceptions.SetupException('max_interchanges', max_interchanges, 'int>=0')
			
		if select_interchange_by not in ['speed','waittime','distance']:
			raise exceptions.SetupException('select_interchange_by', select_interchange_by, '(speed|waittime|distance)')
		
		if not isinstance(use_near_stops, bool):
			raise exceptions.SetupException('use_near_stops', use_near_stops, 'bool')
		
		if walk_speed not in ['normal', 'fast', 'slow']:
			raise exceptions.SetupException('walk_speed', walk_speed, '(normal|fast|slow)')
			
		if not isinstance(with_bike, bool):
			raise exceptions.SetupException('with_bike', with_bike, 'bool')
			
		if not isinstance(use_realtime, bool):
			raise exceptions.SetupException('use_realtime', use_realtime, 'bool')
		
		# Post-Request bauen
		post = {
			'changeSpeed': walk_speed,
			'command': '',
			'coordOutputFormat': 'WGS84',
			'imparedOptionsActive': 1,
			'includedMeans': 'checkbox',
			'itOptionsActive': 1,
			'itdDateDay': (now if time is None else time).day,
			'itdDateMonth': (now if time is None else time).month,
			'itdDateYear': (now if time is None else time).year,
			'itdTimeHour': (now if time is None else time).hour,
			'itdTimeMinute': (now if time is None else time).minute,
			'itdTripDateTimeDepArr': timetype,
			'language': 'de',
			'locationServerActive': 1,
			'maxChanges': max_interchanges,
			'nextDepsPerLeg': 1,
			'outputFormat': 'XML',
			'ptOptionsActive': 1,
			'requestID': 0,
			'routeType': {'speed':'LEASTTIME', 'waittime':'LEASTINTERCHANGE', 'distance':'LEASTWALKING'}[select_interchange_by],
			'sessionID': 0,
			'text': 1993
		}
		post.update(dict([('%s_origin'      % name, value) for name, value in p_origin.items()]))
		post.update(dict([('%s_destination' % name, value) for name, value in p_destination.items()]))
		post.update(dict([('%s_via'         % name, value) for name, value in p_via.items()]))
		
		if use_realtime: post['useRealtime'] = 1
		if use_near_stops: post['useProxFootSearch'] = 1
		if with_bike: post['bikeTakeAlong'] = 1
		
		includes, linerestriction = self.motsExcludeConverter(exclude)
		post.update(dict([('inclMOT_%d' % i, 'on') for i in includes]))
		post['lineRestriction'] = linerestriction
		
		rawdata = self.submit(self.url_triprequest, post)
		result = XMLParser.Request(ET.fromstring(rawdata))
		
		result.interface = self
		result.url  = self.url_triprequest
		result.post = post
		return result
		
	def later(self):
		# fixme
		pass
		
	def earlier(self):
		# fixme
		pass
	pass	

class XMLParser():
	@classmethod
	def Request(self, data):
		for subdata in data:
			if subdata.tag == 'itdTripRequest':
				result = self.TripResult(subdata)
				break
		else:
			result = models.Request()
		
		attrs = data.attrib
		if 'now' in attrs:
			result.dataTime = datetime.datetime.strptime(attrs['now'], '%Y-%m-%dT%H:%M:%S')
			
		if 'version' in attrs:
			result.serverVersion = attrs['version']
			
		if 'sessionID' in attrs:
			result.sessionID = attrs['sessionID']
			
		if 'client' in attrs:
			result.clientAgent = attrs['client']
			
		if 'clientIP' in attrs:
			result.clientIP = attrs['clientIP']
			
		if 'serverID' in attrs:
			result.serverID = attrs['serverID']
			
		return result
		
	@classmethod
	def TripResult(self, data):
		result = models.TripResult()
		
		if 'requestID' in data.attrib:
			result.requestID = data.attrib['requestID']
			
		# DateTime
		tdt = data.find('./itdTripDateTime')
		if tdt:
			result.timetype = tdt.attrib['deparr']
			result.time = self.DateTime(tdt.find('./itdDateTime'))
		
		# Options
		result.include = []
		options = data.find('./itdTripOptions/itdPtOptions')
		if options:
			options = options.attrib
			for name, value in options.items():
				if   name == 'maxChanges':      result.max_interchanges = int(value)
				elif name == 'routeType':       result.select_interchange_by = {'LEASTTIME':'speed', 'LEASTINTERCHANGE':'waittime', 'LEASTWALKING':'distance'}[value]
				elif name == 'changeSpeed':     result.walk_speed = value
				elif name == 'lineRestriction': 
					if value == '400': result.include = ['ice', 'ic', 'local']
					elif value == '401': result.include = ['ic', 'local']
					elif value == '403': result.include = ['local']
				elif name == 'useProxFootSearch': result.use_near_stops = (value == '1')
				elif name == 'bike':              result.with_bike = (value == '1')
				elif name == 'bike':              result.with_bike = (value == '1')
				
		# More Options							
		options = data.find('./itdTripOptions/itdUsedOptions')
		if options:
			options = options.attrib
			for name, value in options.items():
				if name == 'realtime': result.use_realtime = (value == '1')
		
		# Excluded MOTs
		excluded = data.findall('./itdTripOptions/itdPtOptions/excludedMeans/meansElem')
		if excluded:
			result.exclude = []
			for mot in excluded:
				if mot.attrib['value'] == '0' and mot.attrib['selected'] == '0':
					result.exclude += list(set(['ice', 'ic', 'local'])-set(result.include))
				elif mot.attrib['selected'] == '1':
					if mot.attrib['value'] == '0':
						result.exclude += ['ice', 'ic', 'local']
					else:
						result.exclude.append(API.mots[int(mot.attrib['value']+2)])
			result.exclude = tuple(result.exclude)
			result.include = tuple(set(API.mots)-set(result.exclude))
		else:
			result.include = None
			
		# ODVs
		odvs = data.findall('./itdOdv')
		for odv in odvs:
			setattr(result, odv.attrib['usage'], self.ODV(odv))
		if result.via:
			result.via = [result.via] if result.via else []
			
		# Trips, finally!
		routes = data.findall('./itdItinerary/itdRouteList/itdRoute')
		for route in routes:
			pass
		
		return result
		
	@classmethod
	def TripList(self, data):
		
		pass
		
	@classmethod
	def DateTime(self, data):
		d = data.find('./itdDate').attrib
		t = data.find('./itdTime').attrib
		return datetime.datetime(int(d['year']), int(d['month']), int(d['day']), int(t['hour']), int(t['minute']))
		
	@classmethod
	def ODV(self, data):
		odvtype = data.attrib['type']
	
		# Place
		p = data.find('./itdOdvPlace')
		if p.attrib['state'] == 'empty':
			return None
		elif p.attrib['state'] != 'identified':
			result = models.OdvUnclear('city')
			if p.attrib['state'] == 'list':
				pe = p.findall('./odvPlaceElem')
				for item in pe:
					city    = models.City(item.text)
					city.id = int(item.attrib['placeID'])
					result.possibilities.append(place)
			return result
		else:
			pe = p.find('./odvPlaceElem')
			city    = models.City(pe.text)
			city.id = int(pe.attrib['placeID'])
			
		# Location
		n = data.find('./itdOdvName')
		if n.attrib['state'] != 'identified':
			result = models.OdvUnclear('location')
			if n.attrib['state'] == 'list':
				ne = n.findall('./odvNameElem')
				for item in ne:
					if odvtype == 'stop': 
						location = models.Stop(city, item.text)
						location.id = int(item.attrib['stopID'])
						if 'x' in item.attrib:
							location.x = float(item.attrib['x']) / 1000000
							location.y = float(item.attrib['y']) / 1000000
					result.possibilities.append(location)
			return result
		else:
			ne = n.find('./odvNameElem')
			if odvtype == 'stop': 
				location = models.Stop(city, ne.text)
				location.id = int(ne.attrib['stopID'])
				if 'x' in ne.attrib:
					location.x = float(ne.attrib['x']) / 1000000
					location.y = float(ne.attrib['y']) / 1000000
			return location
