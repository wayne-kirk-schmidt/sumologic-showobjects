#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0413

"""
Exaplanation: show_objects

Usage:
   $ python  show_objects [ options ]

Style:
   Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

    @name           show_objects
    @version        2.00
    @author-name    Wayne Schmidt
    @author-email   wschmidt@sumologic.com
    @license-name   Apache 2.0
    @license-url    https://www.apache.org/licenses/LICENSE-2.0
"""

__version__ = 2.00
__author__ = "Wayne Schmidt (wschmidt@sumologic.com)"

import configparser
import json
import os
import sys
import time
import argparse
import http
import requests
sys.dont_write_bytecode = True

import sumologicobjects

CFGDICT = {}

PARSER = argparse.ArgumentParser(description="""
sumocontentmap prints out a map of all content you have in your personal folder
""")

PARSER.add_argument('-c', metavar='<cfgfile>', dest='CONFIG', \
                    default='undefined', help='specify a config file')
PARSER.add_argument("-v", type=int, default=0, metavar='<verbose>', \
                    dest='verbose', help="specify level of verbose output")
PARSER.add_argument("-a", metavar='<secret>', dest='MY_SECRET', \
                    help="set api (format: <key>:<secret>) ")
PARSER.add_argument("-d", metavar='<cache>', dest='CACHED', \
                    default='/var/tmp/sumologicobjects', \
                    help="set api (format: <key>:<secret>) ")

ARGS = PARSER.parse_args()

DELAY_TIME = 1

OBJECTMAP = {}

### main driver ###

def initialize_variables():
    """
    Define and read configuration file, validating config file entries
    """

    if ARGS.MY_SECRET:
        (api_key, api_secret) = ARGS.MY_SECRET.split(':')
        CFGDICT['SUMOUID'] = api_key
        CFGDICT['SUMOKEY'] = api_secret

    if ARGS.CACHED:
        CFGDICT['CACHED'] = ARGS.CACHED

    if ARGS.CONFIG != 'undefined':
        if os.path.exists(ARGS.CONFIG):
            config = configparser.RawConfigParser()
            config.optionxform = str
            config.read(ARGS.CONFIG)
        else:
            print(f'ConfigFile: {ARGS.CONFIG} Missing! Exiting.')
            sys.exit()

        if ARGS.verbose > 8:
            print(dict(config.items('Default')))

        if config.has_option("Default", "CACHED"):
            CFGDICT['CACHED'] = config.get("Default", "CACHED")

        if config.has_option("Default", "SUMOUID"):
            CFGDICT['SUMOUID'] = config.get("Default", "SUMOUID")

        if config.has_option("Default", "SUMOKEY"):
            CFGDICT['SUMOKEY'] = config.get("Default", "SUMOKEY")

    return CFGDICT

def main():
    """
    Setup the Sumo API connection, using the required tuple of region, id, and key.
    Once done, then issue the command required
    """

    initialize_variables()

    source = SumoApiClient(CFGDICT['SUMOUID'], CFGDICT['SUMOKEY'])

    os.makedirs(CFGDICT['CACHED'], exist_ok=True)

    for myobject, myurl in sumologicobjects.OBJECTMAP.items():
        myoutput = source.show_object(myurl)
        if ARGS.verbose > 4:
            print(f'### === {myobject} === ###')
        outputfile = f'{CFGDICT["CACHED"]}/{myobject}.json'
        with open (outputfile, 'w', encoding='utf8') as outputobject:
            outputobject.write(json.dumps(myoutput))

### class ###
class SumoApiClient():
    """
    This is defined SumoLogic API Client
    The class includes the HTTP methods, cmdlets, and init methods
    """

    def __init__(self, access_id, access_key, endpoint=None, cookie_file='cookies.txt'):
        """
        Initializes the Sumo Logic object
        """

        self.session = requests.Session()

        self.session.auth = (access_id, access_key)
        self.session.headers = {'content-type': 'application/json', \
            'accept': 'application/json'}
        cookiejar = http.cookiejar.FileCookieJar(cookie_file)
        self.session.cookies = cookiejar
        if endpoint is None:
            self.endpoint = self._get_endpoint()
        elif len(endpoint) < 3:
            self.endpoint = 'https://api.' + endpoint + '.sumologic.com/api'
        else:
            self.endpoint = endpoint
        if self.endpoint[-1:] == "/":
            raise Exception("Endpoint should not end with a slash character")

    def _get_endpoint(self):
        """
        SumoLogic REST API endpoint changes based on the geo location of the client.
        It contacts the default REST endpoint and resolves the 401 to get the right endpoint.
        """
        self.endpoint = 'https://api.sumologic.com/api'
        self.response = self.session.get('https://api.sumologic.com/api/v1/collectors')
        endpoint = self.response.url.replace('/v1/collectors', '')
        return endpoint

    def delete(self, method, params=None, headers=None, data=None):
        """
        Defines a Sumo Logic Delete operation
        """
        response = self.session.delete(self.endpoint + method, \
            params=params, headers=headers, data=data)
        if response.status_code != 200:
            response.reason = response.text
        response.raise_for_status()
        return response

    def get(self, method, params=None, headers=None):
        """
        Defines a Sumo Logic Get operation
        """
        response = self.session.get(self.endpoint + method, \
            params=params, headers=headers)
        if response.status_code != 200:
            response.reason = response.text
        response.raise_for_status()
        return response

    def post(self, method, data=None, headers=None, params=None):
        """
        Defines a Sumo Logic Post operation
        """
        response = self.session.post(self.endpoint + method, \
            data=json.dumps(data), headers=headers, params=params)
        if response.status_code != 200:
            response.reason = response.text
        response.raise_for_status()
        return response

    def put(self, method, data, headers=None, params=None):
        """
        Defines a Sumo Logic Put operation
        """
        response = self.session.put(self.endpoint + method, \
            data=json.dumps(data), headers=headers, params=params)
        if response.status_code != 200:
            response.reason = response.text
        response.raise_for_status()
        return response

### class ###
### methods ###

    def show_object(self, urlstub):
        """
        Show all of the dashboards
        """
        url = str(urlstub)
        body = self.get(url).text
        results = json.loads(body)
        time.sleep(DELAY_TIME)
        return results

### methods ###

if __name__ == '__main__':
    main()
