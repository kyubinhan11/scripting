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
from key import KEY

BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
MAXIMUM_PAGE = 2

def main(args):
    radius = args.radius if args.radius != None else 5000
    keyword = args.keyword

    LATITUDE = '48.4384'
    LONGITUDE = '-123.365'
    location = LATITUDE + ',' + LONGITUDE
    typeOf = 'restaurant'

    initial_query = {'location': location, 'radius': radius, 'type': typeOf, \
    'keyword': keyword, 'key': KEY}
    
    search_restaurants(initial_query, next_page_token = None, initial_rank = 1, page = 1)

def search_restaurants(initial_query, next_page_token, initial_rank, page):
    """
    Make multiple network calls using recursion
    """
    try:
        query = initial_query    
        if(next_page_token != None):
            query = {'pagetoken': next_page_token, 'key': KEY}    
        req = requests.get(BASE_URL, params = query)

        json_data = req.json() #json_data is a dictionary
        
        number_of_results = print_names_and_rankings(initial_rank, json_data) # the maximum is 20

        if ('next_page_token' in json_data) and (page < MAXIMUM_PAGE):
            # wait a few seconds between consecutive requests for the token to be validated
            sleep(2)
            search_restaurants(initial_query, json_data['next_page_token'], \
            initial_rank + number_of_results, page + 1)

    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print e
        sys.exit(1)

def print_names_and_rankings(initial_rank, json_data):
    """
    Parse json data to print names and rankings 
    
    return the number of results
    """
    if error_handler(json_data):
        return

    # print json.dumps(json_data, indent=2) # for debugging 

    results = json_data['results']
    for i in range(len(results)):
        # encode unicodes to UTF-8 strings
        name = results[i]['name'].encode('utf-8').strip()
        print 'Rank {0}, Name: {1}'.format(initial_rank + i, name)

    return len(results)

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
            print 'Status: {0}, Reference: {1}'.format(status, reference)
            return True
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='searchs for restaurants with a keyword using Google places search API')
    parser.add_argument('keyword', action='store', help='a term to be matched against all content')
    
    parser.add_argument('-r', '--radius',action='store', dest='radius',
                        help='the distance (in meters) within which to return place results')

    args = parser.parse_args()

    main(args)