"""
endpoint examples

https://maps.googleapis.com/maps/api/place/nearbysearch/json
?location=48.4384,-123.365&radius=5000&type=restaurant&keyword=mexican
&key=YOUR_API_KEY

https://maps.googleapis.com/maps/api/place/nearbysearch/json?
pagetoken=CpQCAgEAAFxg8o-eU7_uKn7Yqjana-HQIx1hr5BrT4zBaEko29ANsXtp9mrqN0yrKWhf-y2
PUpHRLQb1GT-mtxNcXou8TwkXhi1Jbk-ReY7oulyuvKSQrw1lgJElggGlo0d6indiH1U-tDwquw4tU_UXoQ_
sj8OBo8XBUuWjuuFShqmLMP-0W59Vr6CaXdLrF8M3wFR4dUUhSf5UC4QCLaOMVP92lyh0OdtF_m_9Dt7lz
-Wniod9zDrHeDsz_by570K3jL1VuDKTl_U1cJ0mzz_zDHGfOUf7VU1kVIs1WnM9SGvnm8YZURLTtMLMWx8
-doGUE56Af_VfKjGDYW361OOIj9GmkyCFtaoCmTMIr5kgyeUSnB-IEhDlzujVrV6O9Mt7N4DagR6RGhT3g
1viYLS4kO5YindU6dm3GIof1Q&key=YOUR_API_KEY

"""
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

def main(args):
    radius = args.radius if args.radius != None else 5000
    keyword = args.keyword
    
    location = LATITUDE + ',' + LONGITUDE

    query = {'location': location, 'radius': radius, \
    'keyword': keyword, 'key': API_KEY}
    
    search_restaurants(query, next_page_token = None, initial_rank = 1, page = 1)


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
            get_more_results(json_data['next_page_token'], initial_rank + MAX_RESULT_PER_PAGE, page + 1)

    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print e
        sys.exit(1)


def get_more_results(next_page_token, initial_rank, page):
    try:
        query = {'pagetoken': next_page_token, 'key': API_KEY}    
        req = requests.get(BASE_URL, params = query)

        json_data = req.json() #json_data is a dictionary
        print_names_and_rankings(initial_rank, json_data) 

        if ('next_page_token' in json_data) and (page < MAX_PAGE):
            # wait a few seconds between consecutive requests for the token to be validated
            sleep(2)
            get_more_results(json_data['next_page_token'], initial_rank + MAX_RESULT_PER_PAGE, page + 1)

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
    #TODO: make it optional
    parser.add_argument('keyword', action='store', help='a term to be matched against all content')
    
    parser.add_argument('-r', '--radius',action='store', dest='radius',
                        help='the distance (in meters) within which to return place results')

    args = parser.parse_args()

    main(args)