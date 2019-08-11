#!/usr/bin/env python3

import requests

# replace with real IP or hostname of the API
host = 'http://9.12.16.57:9950'
cpc = '????'


def main():
    for i in range(1, 9):
        response = requests.post(
            host + '/api/cpcs/' + cpc +'/operations/export-profiles', 
            json={
                'profile-area': i
            }, 
            headers={
                'X-API-Session': '',  # add the session string here
                'host': ''            # What host?
            }
        )

        if response.status_code != 204:
            raise ValueError('Export for profile ' + i + ' has failed: \n' + response)
            
        # move the file from its known location to the 
        moveFile(i)


def moveFile(profile):
    path = '/console/data/iqzweih' + profile + '...'
    # move to repo

    # call github to commit file



if __name__ == "__main__":
    main()