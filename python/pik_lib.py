import os
import re
import json
import requests
import zipfile
import sqlite3
import numpy as np
from datetime import datetime


def load_project_list():
    with open('projects.json', 'r') as f:
        data = json.load(f)
    return data


def download_flats(project, archive_enabled=False):

    def get_ts():
        return datetime.now().strftime('%Y%m%d_%H%M%S')

    result = []
    filenames = []
    
    for i in range(100):
        
        url = 'https://api-selectel.pik-service.ru/v2/filter'
        params = {'block': project['id'],
                  'flatPage': i + 1,
                  'onlyFlats': 1,
                  'sortBy': 'price'}
        url += '?' + '&'.join(k + '=' + str(params[k]) for k in params)
        response = requests.get(url)

        try:
            flats = json.loads(response.content)['blocks'][0]['flats']
        except IndexError:
            break

        for flat in flats:
            d = {'area': flat['area'],
                 'number': flat['number'],
                 'price': flat['price'],
                 'rooms': flat['rooms'],
                 'floor': flat['floor'],
                 'bulk_id': flat['bulk']['id'],
                 'bulk_name': flat['bulk']['name'],
                 'bulk_title': flat['bulk']['title']
                 }
            result.append(d)

        if archive_enabled:
            filename = '../archive/{0}_{1}_{2:02d}.json'.format(get_ts(), project['url'], i)
            with open(filename, 'wb') as f:
                f.write(response.content)

        filenames.append(filename)

    if archive_enabled:
        filename = '../archive/{0}_{1}.zip'.format(get_ts(), project['url'])
        with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as archive:
            for f in filenames:
                archive.write(f, f.split('/')[-1])  # without path
                os.remove(f)

    if archive_enabled:
        filename = '../archive/{0}_{1}.json'.format(get_ts(), project['url'])
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
    
    return result


def download_project_list():

    url = 'https://api.pik.ru/v2/filter?sort=blocks&onlyBlocks=1'
    response = requests.get(url)

    project_list = []
    for project in json.loads(response.content):
        project_list.append({'id': project['id'],
                             'name': project['name'],
                             'url': project['url']})
    return project_list

