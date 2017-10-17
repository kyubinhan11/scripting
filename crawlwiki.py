import argparse
import requests

def main(args):
    isCaseSensitive = args.isCaseSensitive
    website_link = args.website_link if args.website_link != None else 'https://en.wikipedia.org/wiki/Oktoberfest' 
    word = args.word

    # TODO: error handling
    req = requests.get(website_link)
    
    if(isCaseSensitive):
        # Return the number of (non-overlapping) occurrences of substring in the string. 
        print req.text.count(word)

    # case-insentive search
    else: 
        lowercased_text = req.text.lower()
        lowercased_word = word.lower()
        print lowercased_text.count(lowercased_word)
    
    print isCaseSensitive, website_link, word


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='crawl a webpage and count the occurrences of a specified word')
    
    parser.add_argument('-l', '--link',action='store', dest='website_link',
                        help='set the link of the target website')
    
    parser.add_argument('word', action='store', help='a target word')

    parser.add_argument('-c', action='store_true', default = False,
                    dest='isCaseSensitive', 
                    help='set to true for a case-sensitive search')

    args = parser.parse_args()

    main(args)
