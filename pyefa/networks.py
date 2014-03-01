#!/usr/bin/env python
# -*- coding: utf-8 -*-
import efa, exceptions

supported = ('vrr')

class VRR(efa.EFA):
	efa_triprequest_url = 'http://efa.vrr.de/vrr/XSLT_TRIP_REQUEST2'
	
def network(network):
	global supported
	if network not in supported:
		return None
	return globals()[network.upper()]()
