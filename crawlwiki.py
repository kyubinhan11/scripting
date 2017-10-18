import argparse
import requests
import sys

def main(args):
    is_case_sensitive = args.is_case_sensitive
    website_link = args.website_link if args.website_link != None else 'https://en.wikipedia.org/wiki/Oktoberfest' 
    word = args.word

    # print is_case_sensitive, website_link, word

    try:
        req = requests.get(website_link)

        word_count = get_occurrences(is_case_sensitive, req.text, word)
        print 'The word "{0}" occurs {1} times on {2} webpage'.format(word, word_count, website_link) 

    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print e
        sys.exit(1)

def get_occurrences(is_case_sensitive, text, word):
    if(is_case_sensitive):
        # Return the number of (non-overlapping) occurrences of substring in the string. 
        return text.count(word)

    # case-insentive search
    else: 
        lowercased_text = text.lower()
        lowercased_word = word.lower()
        return lowercased_text.count(lowercased_word)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='crawl a webpage and count the occurrences of a specified word')
    
    parser.add_argument('-l', '--link',action='store', dest='website_link',
                        help='set the link of the target website')
    
    parser.add_argument('word', action='store', help='a target word')

    parser.add_argument('-c', action='store_true', default = False,
                    dest='is_case_sensitive', 
                    help='set true for a case-sensitive search')

    args = parser.parse_args()

    main(args)
