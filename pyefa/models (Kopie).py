#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

class Request:
	def __init__(self):
		self.time = datetime.datetime.now()
	
class TripRequest(Request):
	def __init__(self):
		pass

	
