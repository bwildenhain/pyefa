#!/usr/bin/env python3
import efa, exceptions, models

supported = ('vrr', 'vrn')

class VRR(efa.API):
	url_triprequest = 'http://efa.vrr.de/vrr/XSLT_TRIP_REQUEST2'

class VRN(efa.API):
	url_triprequest = 'http://fahrplanauskunft.vrn.de/vrn/XSLT_TRIP_REQUEST2'
	
def network(network):
	global supported
	if network not in supported:
		return None
	return globals()[network.upper()]()

vrr = VRR()
vrr.tripRequest(models.Stop('Essen', 'Hbf'), models.Stop('Duisburg', 'Hbf'))
