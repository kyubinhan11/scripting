#!/usr/bin/python

import requests
import argparse
import json
from time import sleep
from key import API_KEY

BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
LATITUDE = '48.4384'
LONGITUDE = '-123.365'
MAX_RESULT_PER_PAGE = 20
MAX_PAGE = 2
DEFAULT_RADIUS = 5000

def main(args):
    query = build_query(args)
    search_restaurants(query, next_page_token = None, initial_rank = 1, page = 1)


def build_query(args):
    """
    Build a query required for Google Place Search API
    """

    query = {'key': API_KEY}

    radius = args.radius if args.radius != None else DEFAULT_RADIUS
    query['radius'] = radius

    if args.keyword != None:
        query['keyword'] = args.keyword

    location = LATITUDE + ',' + LONGITUDE
    query['location'] = location

    return query


def search_restaurants(query, next_page_token, initial_rank, page):
    """
    Make network calls to get a list of names and ranks of restaurants 
    """
    
    query['type'] = 'restaurant'

    try:
        req = requests.get(BASE_URL, params = query)

        json_data = req.json() #json_data is a dictionary
        
        print_names_and_rankings(initial_rank, json_data) 

        if ('next_page_token' in json_data):
            # wait a few seconds between consecutive requests for the token to be validated
            sleep(2)
            print_more_results(json_data['next_page_token'], initial_rank + MAX_RESULT_PER_PAGE, page + 1)

    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print e
        sys.exit(1)


def print_more_results(next_page_token, initial_rank, page):
    """
    Get more results when intial results are more than 20
    """
    try:
        query = {'pagetoken': next_page_token, 'key': API_KEY}    
        req = requests.get(BASE_URL, params = query)

        json_data = req.json() #json_data is a dictionary
        print_names_and_rankings(initial_rank, json_data) 

        if ('next_page_token' in json_data) and (page < MAX_PAGE):
            # wait a few seconds between consecutive requests for the token to be validated
            sleep(2)
            print_more_results(json_data['next_page_token'], initial_rank + MAX_RESULT_PER_PAGE, page + 1)

    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print e
        sys.exit(1)


def print_names_and_rankings(initial_rank, json_data):
    """
    Parse json data to print names and rankings of each results
    """
    if error_handler(json_data):
        return

    # print json.dumps(json_data, indent=2) # for debugging 

    results = json_data['results']
    for i in range(len(results)):
        # encode unicodes to UTF-8 bytes then decode it back to get the symbol
        name = results[i]['name'].encode('utf-8').decode('utf-8')
        print 'Rank %s, %s' % (initial_rank + i, name)
        

def error_handler(json_data):
    """
    Check to see if there is an error message or bad status other than 'OK'
    
    return boolean 
    """
    if 'error_message' in json_data:
        print json_data['error_message']
        return True

    if 'status' in json_data:
        status = json_data['status']
        if status != 'OK':
            reference = 'https://developers.google.com/places/web-service/search#PlaceSearchStatusCodes'
            print 'Status: %s, Reference: %s' % (status, reference)
            return True
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='searchs for restaurants with a keyword using Google places search API')

    parser.add_argument('keyword', action='store', nargs='?', help='a term to be matched against all content')
    
    parser.add_argument('-r', '--radius', action='store', dest='radius',
                        help='the distance (in meters) within which to return place results')

    args = parser.parse_args()

    main(args)