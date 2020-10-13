import csv
import os
import json
import requests
import shutil
import time
import random
import re


KEYS = 'KEYS'
BASE_DIR = '../ads/products'
DAYS = 14
PARTIES = {'(D)': 'Democrat', '(R)': 'Republican'}

REP_CANDIDATE_QUERY = 'https://api.open.fec.gov/v1/candidates/search/' \
                  '?candidate_status=C&election_year=2018&sort=district' \
                  '&per_page=100&api_key={}&state={}&party=REP&office={}'
DEM_CANDIDATE_QUERY = 'https://api.open.fec.gov/v1/candidates/search/' \
                  '?candidate_status=C&election_year=2018&sort=district' \
                  '&per_page=100&api_key={}&state={}&party=DEM&office={}'
PRODUCT_QUERY = 'https://api.bestbuy.com/v1/products(artistName={}*&type=Music)' \
                '?apiKey={}&format=json&show=artistName,format,image,url,details.value'


EASTERN_STATES = {'NJ': 'New Jersey', 'CT': 'Connecticut', 'VT': 'Vermont',
                  'NC': 'North Carolina', 'SC': 'South Carolina', 'ME': 'Maine', 'NH': 'New Hampshire',
                  'RH': 'Rhode Island', 'VA': 'Virginia', 'GA': 'Georgia', 'FL': 'Florida', 'NY': 'New York'}
WESTERN_STATES = {'OR': 'Oregon', 'WA': 'Washington', 'NV': 'Nevada',
                  'UT': 'Utah', 'ID': 'Idaho', 'CA': 'California'}

EASTERN_KEYWORDS = 'east coast, record store, vinyl, cd'
WESTERN_KEYWORDS = 'west coast, record store, vinyl, cd'
NATIONAL_KEYWORDS = 'record store, vinyl, cd'


def get_congress_candidates (api_key, affiliation, states, offices):
    """
    Get a list of Congressional candidates from the OpenFEC API
    https://api.open.fec.gov/developers/ 
    """
    # Get the surname, voting district, and party affiliation of each candidate in a given state
    candidates = []
    for office in offices:
        for state in states:
            print(state, office)
            if affiliation == 'Democrat':
                query = DEM_CANDIDATE_QUERY.format(api_key, state, office)
            elif affiliation == 'Republican':
                query = REP_CANDIDATE_QUERY.format(api_key, state, office)
            else:
                print('Not a valid political affiliation')
                exit(-1)
                
            response = requests.get(query).json()
            for candidate in response['results']:
                surname = candidate['name'].split(', ')[0]
                party = candidate['party']
                district = candidate['district']
                candidate_info = (surname, party, state, district, office)
                print(candidate_info)
                candidates.append(candidate_info)
            print()
    return candidates


def get_gubernatorial_candidates(affiliation):
    """Parse a CSV of gubernatorial candidates"""
    results = []
    with open('gubernatorial.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            # Clean the data up
            candidates = row[5]
            no_citations = re.sub(r'\[([0-9]*)\]', '', candidates)
            add_spaces = re.sub(r'\)', ')|', no_citations)
            candidates_list = add_spaces.split('|')

            # Find candidates that match desired affiliation
            desired_candidates = [c for c in candidates_list if affiliation in c]
            if len(desired_candidates) == 0:
                continue
            else:
                candidate = desired_candidates[0]

            # Add candidate info to list
            candidate = candidate.replace(affiliation, '')
            surname = candidate.split(' ')[-2]
            party = PARTIES[affiliation]
            state = row[0]
            district = 'n/a'
            office = 'Governor'
            candidate_info = (surname, party, state, district, office)
            print(candidate_info)
            results.append(candidate_info)
        print()
    return results


def get_products (api_key, surname):
    """
    Get a list of products that share a candidate's name from the Best Buy API
    https://developer.bestbuy.com/
    """
    query = PRODUCT_QUERY.format(surname.title(), api_key)
    response = requests.get(query).json()
    time.sleep(0.1)
    products = []

    # Search for music CDs/LPs which have a candidate's surname in the artist name
    if response and response['products']:
        for product in response['products']:
            artistName = product['artistName']
            if surname.lower() in artistName.lower().split() and product['details']:
                products.append({'surname': surname, 'artist': artistName,
                                 'image': product['image'], 'format': product['format'],
                                 'url': product['url']})
    return products


def gen_congress_ads (bestbuy_key, candidates, affiliation, dir_name, states):
    """Generate ads for Congressional condidates"""
    # Create a directory for the state
    ad_dir = BASE_DIR + '/' + affiliation + '/' + dir_name
    if not os.path.exists(ad_dir):
        os.makedirs(ad_dir)
    else:
        shutil.rmtree(ad_dir)

    ads = []
    for candidate in candidates:
        # If there are already 20 ads, stop collecting
        if len(ads) > 20:
            ads = ads[:20]
            break
        
        # Get product info based on the candidate's surname
        surname = candidate[0]
        party = candidate[1]
        state_code = candidate[2]
        district = candidate[3]
        office = candidate[4]
        products = get_products(bestbuy_key, surname=surname)
        if products:
            # Get the text info for the ad
            product = products[0]
            image_url = product['image']
            if not image_url:
                continue
            
            body = 'Check out this {} from the one and only {}!'
            body = body.format(product['format'], surname.title()) 
            website = product['url']           
            headline = 'Calling all music lovers'
            if states == EASTERN_STATES:
                ad = 'Text: {}, Website URL: {}, Headline: {}, State: {}, District: {}, ' \
                     'Office: {}, Keywords: {}'.format(body, website, headline, state_code,
                                                       district, office, EASTERN_KEYWORDS)
                ads.append((surname, ad, product['image'], state_code))
            elif states == WESTERN_STATES:
                ad = 'Text: {}, Website URL: {}, Headline: {}, State: {}, District: {}, ' \
                     'Office: {}, Keywords: {}'.format(body, website, headline, state_code,
                                                       district, office, WESTERN_KEYWORDS)
                ads.append((surname, ad, product['image'], state_code))
    return (ads, ad_dir)


def gen_gubernatorial_ads (bestbuy_key, candidates, affiliation, dir_name, dir_id):
    """Generate ads for gubernatorial candidates"""
    # Create a directory for the state
    ad_dir = BASE_DIR + '/' + affiliation + '/' + dir_name
    if not os.path.exists(ad_dir):
        os.makedirs(ad_dir)
    else:
        shutil.rmtree(ad_dir)

    ads = []
    for candidate in candidates:
        # If there are already 20 ads, stop collecting
        if len(ads) > 20:
            ads = ads[:20]
            break
        
        # Get product info based on the candidate's surname
        surname = candidate[0]
        party = candidate[1]
        state = candidate[2]
        district = candidate[3]
        office = candidate[4]
        products = get_products(bestbuy_key, surname=surname)
        if products and len(products) >= 2:
            if dir_id == 1:
                products = products[:int(len(products)/2)]
            elif dir_id == 2:
                products = products[int(len(products)/2):]
                
            # Get the text info for the ad
            for product in products:
                image_url = product['image']
                if not image_url:
                    continue

                body = 'Check out this {} from the one and only {}!'
                body = body.format(product['format'], surname.title()) 
                website = product['url']           
                headline = 'Calling all music lovers'
                ad = 'Text: {}, Website URL: {}, Headline: {}, State: {}, District: {}, ' \
                     'Office: {}, Keywords: {}'.format(body, website, headline, state, district,
                                                       office, NATIONAL_KEYWORDS)
                ads.append((surname, ad, product['image'], state))
    return (ads, ad_dir)


def write_ads(ads, ad_dir):
    """Write ads to disk"""
    # Randomly choose days where 2 ads will be placed
    double_days = random.sample(range(1,15), 6)
    print('Days where two ads will be placed:', double_days)
    
    i = 0
    for day in range(1, DAYS + 1):
        # Make a subdirectory for eacb day of ad placements        
        day_dir = ad_dir + '/' + 'Day {}'.format(day)
        if not os.path.exists(day_dir):
            os.makedirs(day_dir)
        else:
            shutil.rmtree(day_dir)

        # Write an ad to disk
        write_one_ad(ads[i], day_dir)
        i += 1

        # If a double day, write another ad
        if day in double_days:
            write_one_ad(ads[i], day_dir)
            i += 1


def write_csv(ads, ad_dir, affiliation, targeting):
    """Write a CSV template to disk for participants to fill out"""
    with open(ad_dir + '/' + 'spreadsheet.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|',
                                quotechar='\'', quoting=csv.QUOTE_MINIMAL)

        # Write the header, and then write a row for each ad (with some columns to be filled in later)
        csvwriter.writerow(['Ad Poster ID', 'Date', 'Ad ID', 'Platform', 'Ad ' \
                            'Name', 'Text', 'Location', 'Left or right' \
                            'leaning?', 'Product or Issue-reference?',
                            'State or National candidate/issue?', 'Ad ' \
                            'Permitted (Y/N)', 'Platform Attempted to Verify My ' \
                            'Account Before This Point (Y/N)',
                            'Platform successfully verified my account before this point (Y/N) ',                
                            'Platform listed transparency info with ad' \
                            '(Y/N)', 'Ad Removed Within 48 Hours (Y/N)',
                            '48 Hour Results', '48 Hour Reach', '48 Hour Impressions'])

        for ad in ads:
            csvwriter.writerow(['', '', '', 'Facebook', ad[0], ad[1], ad[3], affiliation,
                                'Product', targeting, '', '', '', '', '', '', '', ''])
            csvwriter.writerow(['', '', '', 'Google', ad[0], ad[1], ad[3], affiliation,
                                'Product', targeting, '', '', '', '', '', '', '', ''])


def write_one_ad(ad_tuple, day_dir):
    """Write a single ad to disk"""
    surname = ad_tuple[0]
    ad = ad_tuple[1]
    image_url = ad_tuple[2]
    img_data = requests.get(image_url).content

    # Write the image to disk
    with open(day_dir + '/' + surname.title() + '.jpg', 'wb') as img:
        img.write(img_data)

    # Write the ad text to disk
    with open (day_dir + '/' + surname.title() + '.txt', 'w') as txt:
        txt.write(ad)
    print(ad + '\n')

    
if __name__ == '__main__':
    # Load API keys from disk
    with open(KEYS) as f:
        keys = json.load(f)

    # Generate ads for current Congressional candidates
    # candidates = get_congress_candidates(keys['FEC'], affiliation='Democrat',
    #                             states=WESTERN_STATES, offices=['H', 'S'])

    # ads_tuple = gen_congress_ads(keys['BEST_BUY'], candidates, 'Democrat',
    #                              'Congressional Candidates (D) #1', WESTERN_STATES)
    # ads = ads_tuple[0]
    # ad_dir = ads_tuple[1] 
    # write_ads(ads, ad_dir)
    # write_csv(ads, ad_dir, 'Democrat', 'National')


    # Generate ads for current gubarnatorial candidates
    candidates = get_gubernatorial_candidates(affiliation='(D)')
    ads_tuple = gen_gubernatorial_ads(keys['BEST_BUY'], candidates, 'Democrat',
                                      'Gubernatorial Candidates (D) #1', 1)
    ads = ads_tuple[0]
    ad_dir = ads_tuple[1] 
    write_ads(ads, ad_dir)
    write_csv(ads, ad_dir, 'Democrat', 'State')
