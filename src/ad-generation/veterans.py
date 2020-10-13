import csv
import os
import json
import requests
import shutil
import random
from bs4 import BeautifulSoup


KEYS = 'KEYS'
BASE_DIR = '../ads/issues/Republican'
DAYS = 14

PARADES_URL = 'https://www.vetfriends.com/parades/directory.cfm?state={}'

AD_TEXT = 'Don\'t forget about our troops. Visit the {}.'
AD_HEADLINE = 'Respect our military this November'


EASTERN_STATES = ['CT', 'VT', 'NC', 'SC', 'ME', 'DE', 'MA', 'NH', 'RI', 'VA', 'GA', 'FL', 'NY', 'NJ']
WESTERN_STATES = ['OR', 'WA', 'NV', 'UT', 'ID', 'CA']

EASTERN_KEYWORDS = 'east coast, veterans day, parades'
WESTERN_KEYWORDS = 'west coast, veterans day, parades'


def get_parades (states):
    """Get a list of Veteran's Day parades from www.vetfriends.com"""
    # Scrape the name of each parade
    parades = []
    for state in states:
        # GET the webpage for Veterans Day parades in a given state
        query = PARADES_URL.format(state)    
        response = requests.get(query).content
        soup = BeautifulSoup(response, 'html.parser')        
        events = soup.find_all('table', {'cellpadding': '5', 'cellspacing': '5', 'width': '100%'})
        for event in events:
            name = event.center.string.title().split('/')[0].strip()
            parades.append((name, state))
    return parades


def gen_ads (dir_name, states):
    """Generate a Veteran's Day ad for parades from each state"""
    # Create the directory for the ad data
    ad_dir = BASE_DIR + '/' + dir_name
    if not os.path.exists(ad_dir):
        os.makedirs(ad_dir)
    else:
        shutil.rmtree(ad_dir)
    
    ads = []
    parades = get_parades(states)
    for parade in parades:
        if len(ads) > 20:
            break
        
        # Get the ad info
        name = parade[0]
        state = parade[1]
        text = AD_TEXT.format(name)
        website = PARADES_URL.format(state)
        if states == EASTERN_STATES:
            ad = 'Text: {}, Website URL: {}, Headline: {}, State: {}, Keywords: {}'.format(text, website, 
                                                                                           AD_HEADLINE, state,
                                                                                           EASTERN_KEYWORDS)
        elif states == WESTERN_STATES:
            ad = 'Text: {}, Website URL: {}, Headline: {}, State: {}, Keywords: {}'.format(text, website,
                                                                                           AD_HEADLINE, state,
                                                                                           WESTERN_KEYWORDS)
        ads.append((name, ad, 'n/a', state))
    return (ads, ad_dir)


def write_ads (ads, ad_dir):
    """Write the ads to disk"""
    # Randomly choose days where 2 ads will be placed
    double_days = random.sample(range(1,15), 6)
    print('Days where two ads will be placed:', double_days)

    i = 0
    folders = []
    for day in range(1, DAYS + 1):
        # Make a subdirectory for eacb day of ad placements        
        day_dir = ad_dir + '/' + 'Day {}'.format(day)
        if not os.path.exists(day_dir):
            os.makedirs(day_dir)
        else:
            shutil.rmtree(day_dir)

        # Write an ad to disk
        write_one_ad(ads[i], day_dir)
        folders.append((ads[i], day_dir))        
        i += 1

        # If a double day, write another ad
        if day in double_days:
            write_one_ad(ads[i], day_dir)
            folders.append((ads[i], day_dir))
            i += 1
    return folders


def write_one_ad(ad_tuple, day_dir):
    """Write a single ad to disk"""
    # Write the ad to disk only if the ad image exists
    name = ad_tuple[0]
    ad = ad_tuple[1]

    # Write the ad text to disk
    with open(day_dir + '/' + name + '.txt', 'w') as txt:
        txt.write(ad)
    print(ad + '\n')


def write_csv(ad_tuples, ad_dir, affiliation, targeting):
    """Write a CSV template to disk for participants to fill out"""
    with open(ad_dir + '/' + 'spreadsheet.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|',
                                quotechar='\'', quoting=csv.QUOTE_MINIMAL)  
            
        # Write the header, and then write a row for each ad (with some columns to be filled in later)
        csvwriter.writerow(['Ad Poster ID', 'Date', 'Ad ID', 'Folder', 'Platform', 'Ad ' \
                            'Name', 'Text', 'Location', 'Left or right' \
                            'leaning?', 'Product or Issue-reference?',
                            'State or National candidate/issue?', 'Ad ' \
                            'Permitted (Y/N)', 'Platform Attempted to Verify My ' \
                            'Account Before This Point (Y/N)',
                            'Platform successfully verified my account before this point (Y/N) ',                
                            'Platform listed transparency info with ad' \
                            '(Y/N)', 'Ad Removed Within 48 Hours (Y/N)',
                            '48 Hour Results', '48 Hour Reach', '48 Hour Impressions'])

        for ad_tuple in ad_tuples:
            ad = ad_tuple[0]
            day_dir = ad_tuple[1]
            csvwriter.writerow(['', '', '', day_dir, 'Facebook', ad[0], ad[1], ad[3], affiliation,
                                'Issue', targeting, '', '', '', '', '', '', '', ''])
            csvwriter.writerow(['', '', '', day_dir, 'Google', ad[0], ad[1], ad[3], affiliation,
                                'Issue', targeting, '', '', '', '', '', '', '', ''])

if __name__ == '__main__':
    # Generate ads for parks that reference climate change
    ad_tuple = gen_ads('Western U.S. Parades', WESTERN_STATES)
    ads = ad_tuple[0]
    base_dir = ad_tuple[1]

    ads_with_folders = write_ads(ads, base_dir)
    write_csv(ads_with_folders, base_dir, 'Republican', 'State')
    
