#!/usr/bin/env python
# -*- coding: utf-8 -*-
import efa, exceptions

supported = ('vrr', 'vrn')

class VRR(efa.EFA):
	efa_triprequest_url = 'http://efa.vrr.de/vrr/XSLT_TRIP_REQUEST2'

class VRN(efa.EFA):
	efa_triprequest_url = 'http://fahrplanauskunft.vrn.de/vrn/XSLT_TRIP_REQUEST2'
	
def network(network):
	global supported
	if network not in supported:
		return None
	return globals()[network.upper()]()
