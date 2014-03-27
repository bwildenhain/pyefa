#!/usr/bin/env python
import models
import datetime

class API(models.API):
	url_triprequest = None
	def __init__(self):
		pass
		
	def locationConverter(self, location):
		if location is None:
			return {'type': 'stop', 'place': '', 'name': ''}
		elif not isinstance(location, models.Location):
			return None
		elif isinstance(location, models.Stop):
			return {'type': location.name, 'place': location.city.name, 'name': location.name}
		
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
			
		#if not isinstance(exclude, list) or len(set(exclude)-set(self.mots)):
		#	raise exceptions.SetupException('exclude', exclude, 'list with (zug|s-bahn|u-bahn|stadtbahn|tram|stadtbus|regionalbus|schnellbus|seilbahn|schiff|ast|sonstige)')
			
		if not isinstance(max_interchanges, int) or max_interchanges < 0:
			raise exceptions.SetupException('max_interchanges', max_interchanges, 'int>=0')
			
		if select_interchange_by not in ['speed','waittime','distance']:
			raise exceptions.SetupException('select_interchange_by', select_interchange_by, '(speed|waittime|distance)')
		
		if not isinstance(use_near_stops, bool):
			raise exceptions.SetupException('use_near_stops', use_near_stops, 'bool')
			
		#if train_type not in ['local', 'ic', 'ice']:
		#	raise exceptions.SetupException('train_type', train_type, '(local|ic|ice)')
		
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
			'inclMOT_0': 'on',
			'inclMOT_1': 'on',
			'inclMOT_2': 'on',
			'inclMOT_3': 'on',
			'inclMOT_4': 'on',
			'inclMOT_5': 'on',
			'inclMOT_6': 'on',
			'inclMOT_7': 'on',
			'inclMOT_8': 'on',
			'inclMOT_9': 'on',
			'inclMOT_10': 'on',
			'inclMOT_11': 'on',
			'includedMeans': 'checkbox',
			'itOptionsActive': 1,
			'itdDateDay': (now if time is None else time).day,
			'itdDateMonth': (now if time is None else time).month,
			'itdDateYear': (now if time is None else time).year,
			'itdTimeHour': (now if time is None else time).hour,
			'itdTimeMinute': (now if time is None else time).minute,
			'itdTripDateTimeDepArr': timetype,
			'language': 'de',
			#'lineRestriction': {'local':403, 'ic':401, 'ice':400}[train_type],
			'lineRestriction': 403,
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
		#for item in exclude: post.pop('inclMOT_%d' % self.mots.index(item))
		
		#settings = locals()
		#settings.pop('self')
		
		#result = classes.TripResult(settings)
		#result.time = (now if time is None else time)
		print(post)
		
		rawdata = self.submit(self.url_triprequest, post)
			
		#return result
		
	def later(self):
		# fixme
		pass
		
	def earlier(self):
		# fixme
		pass
	pass	

class XMLParser():
	@classmethod
	def TripResult(self, form, to, via, ):
		datetime = EFADateTime.fromxml()
		
		return models.TripResult()	
