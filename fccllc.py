#!/usr/bin/env python

# fcc-lat-lon-county
# copyright (C) 2018 J.W. Crockett, Jr.
# basic lib to query the FCC Census Area API with a latitude and longitude and get 
# back what US state and county or county-level division it belongs to, with simple 
# rate limiting to help avoid the banhammer.  
# Issue: right now assumes that if it sent two numbers in and no results came back, 
# it's a non-US location. Actual error handling TK.
# see https://geo.fcc.gov/api/census/#!/area/get_area for API docs.

import urllib2, json, numbers, time

HOST_URL = "https://geo.fcc.gov/"

RATE_PER_SEC = 1
last_call_time = None

def location(lat,lon):
	
	global last_call_time
	
	if not (isinstance(lat,numbers.Real) and isinstance(lon,numbers.Real)):
		raise BadLatLonException
	
	ENDPOINT = "api/census/area"
	
	if last_call_time:
		delay = time.time() - last_call_time
		if (delay < (1.0/RATE_PER_SEC)):
			time.sleep(delay)
		last_call_time = time.time()
	
	last_call_time = time.time()
	
	fh = urllib2.urlopen(HOST_URL + ENDPOINT + "?lat=" + str(lat) + "&lon=" + str(lon))
	return json.loads(fh.read())
	
def get_county(lat,lon):
	js = location(lat,lon)
	
	if not js["results"]:
		raise NonUSException
		
	return {'state':js["results"][0]["state_name"],'county':js["results"][0]['county_name']}

class NonUSException(Exception):
	pass

class BadLatLonException(Exception):
	pass