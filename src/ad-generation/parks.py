import os
import json
import requests
import shutil
import random
import csv


KEYS = 'KEYS'
BASE_DIR = '../ads/issues/Democrat'
DAYS = 14

PARK_QUERY = 'https://api.nps.gov/api/v1/parks?designation=National%20Park' \
             '&q=National%20Park&stateCode={}&fields=images&limit=40&api_key={}'

PARK_TEXT = 'Visit the {} before it\'s destroyed by climate change!'
PARK_HEADLINE = 'Don\'t forget about nature'

EASTERN_STATES = ['CT', 'VT', 'NC', 'SC', 'ME', 'DE', 'MA', 'NH', 'RI', 'VA', 'GA', 'FL', 'NY', 'NJ']
WESTERN_STATES = ['OR', 'WA', 'NV', 'UT', 'ID', 'CA']

EASTERN_KEYWORDS = 'east coast, national parks, nature'
WESTERN_KEYWORDS = 'west coast, national parks, nature'

  
def get_parks (nps_key, states):
    """
    Get a list of national parks for each state from the National Park Service API
    https://www.nps.gov/subjects/digital/nps-data-api.htm
    """
    parks = []
    names = []
    for state in states:
        query = PARK_QUERY.format(state, nps_key)
        response = requests.get(query).json()
        data = response['data']
        for d in data:
            name = d['fullName']
            if name in names:
                continue
            names.append(name)
            
            if not d['images']:
                continue
            image = d['images'][0]['url']
            url = d['url']
            park = (name, url, image, state)
            parks.append(park)
    return parks


def gen_ads (nps_key, dir_name, states):
    """Main code for generating ads"""
    # Create the directory for the ad data
    ad_dir = BASE_DIR + '/' + dir_name
    if not os.path.exists(ad_dir):
        os.makedirs(ad_dir)
    else:
        shutil.rmtree(ad_dir)
        
    ads = []
    parks = get_parks(nps_key, states)
    for park in parks:
        # Get the text info for the ad
        name = park[0]
        website_url = park[1]
        park_image = park[2]
        state = park[3]
        text = PARK_TEXT.format(name)
        if states == EASTERN_STATES:
            ad = 'Text: {}, Website URL: {}, Headline: {}, State: {}, Keywords: {}'.format(text, website_url,
                                                                                           PARK_HEADLINE, state,
                                                                                           EASTERN_KEYWORDS)
        elif states == WESTERN_STATES:
            ad = 'Text: {}, Website URL: {}, Headline: {}, State: {}, Keywords: {}'.format(text, website_url,
                                                                                PARK_HEADLINE, state,
                                                                                WESTERN_KEYWORDS)
        ads.append((name, ad, park_image, state))
    return (ads, ad_dir)


def write_ads (ads, ad_dir):
    """Write generated ads to disk"""
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


def write_one_ad(ad_tuple, day_dir):
    """Write a single ad to disk"""
    # Write the ad to disk only if the ad image exists
    name = ad_tuple[0]
    ad = ad_tuple[1]
    image_url = ad_tuple[2]
    img_data = requests.get(image_url).content

    # Write the image to disk
    with open(day_dir + '/' + name + '.jpg', 'wb') as img:
        img.write(img_data)

    # Write the ad text to disk
    with open(day_dir + '/' + name + '.txt', 'w') as txt:
        txt.write(ad)
    print(ad + '\n')


def write_csv(ads, ad_dir, affiliation, targeting):
    """Write the CSV template to disk for participants to fill out"""
    with open(ad_dir + '/' + 'spreadsheet.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|',
                                quotechar='\'', quoting=csv.QUOTE_MINIMAL)  

        # Write the header, and then write a row for each ad (with some columns to be filled in later)
        csvwriter.writerow(['Ad Poster ID', 'Date', 'Ad ID', 'Platform', 'Ad' \
                            'Name', 'Text', 'Location', 'Left or right' \
                            'leaning?', 'Product or Issue-reference?',
                            'State or National candidate/issue?', 'Ad' \
                            'Permitted (Y/N)', 'Platform Verified My' \
                            'Account Before This Point (Y/N)',
                            'Platform listed transparency info with ad' \
                            '(Y/N)', '48 Hour Results', '48 Hour Reach',
                            '48 Hour Impressions'])

        for ad in ads:
            csvwriter.writerow(['', '', '', 'Facebook', ad[0], ad[1], ad[3], affiliation,
                                'Product', targeting, '', '', '', '', '', ''])
            csvwriter.writerow(['', '', '', 'Google', ad[0], ad[1], ad[3], affiliation,
                                'Product', targeting, '', '', '', '', '', ''])            

if __name__ == '__main__':
    # Load API keys from disk
    with open(KEYS) as f:
        keys = json.load(f)
    nps_key = keys['NPS_KEY']

    # Generate ads for parks that reference climate change
    ad_tuple = gen_ads(nps_key, 'Western U.S. National Parks', WESTERN_STATES)
    ads = ad_tuple[0]
    ad_dir = ad_tuple[1]
    write_ads(ads, ad_dir)
    write_csv(ads, ad_dir, 'Democrat', 'State')
