import os
import re
import json
import requests
import zipfile
import sqlite3
import numpy as np
from datetime import datetime


class Database:

    filename = '../database/database.db'
    timestamp_margin = 300

    def __init__(self):

        if not os.path.isdir('../database'):
            os.mkdir('../database')

        need_to_initialize = False
        if os.path.isfile(self.filename):
            print('Database found')
        else:
            need_to_initialize = True
            print('Database not found')
            print('Creating new database')

        self.conn = sqlite3.connect(self.filename)
        self.cursor = self.conn.cursor()

        if need_to_initialize:
            self.cursor.execute('''
                      CREATE TABLE IF NOT EXISTS flats
                      ([record_id] INTEGER PRIMARY KEY,
                      [project] TEXT,
                      [flat_id] INTEGER,
                      [area] REAL,
                      [number] INTEGER,
                      [price] INTEGER,
                      [rooms] INTEGER,
                      [floor] INTEGER,
                      [bulk_id] INTEGER,
                      [bulk_title] TEXT,
                      [timestamp] INTEGER
                      )
                      ''')            
            self.save_changes()

    def get_price_timeline(self, flat_id):
        q = """
        SELECT timestamp, price
        FROM flats
        WHERE flat_id={0}
        ORDER BY timestamp
        """.format(flat_id)
        res = self.cursor.execute(q).fetchall()
        timestamps = [r[0] for r in res]
        price = [r[1] for r in res]
        return timestamps, price

    def write(self, flat):
        q_parameters = ','.join(flat.keys())
        q_values = ','.join( [ "'"+i+"'" if type(i) is str
                               else str(i)
                               for i in flat.values()] )
        self.cursor.execute('''
                            INSERT INTO flats ({0})
                            VALUES({1});
                            '''.format(q_parameters, q_values))

    def request(self, request):
        res = self.cursor.execute(request).fetchall()
        return res

    def get_daily_report(self, project, days_ago=0):
        q = """
        SELECT rooms, COUNT(*)
        FROM flats
        WHERE date(timestamp, 'unixepoch')=date('now', '-{0} day')
        AND project='{1}'
        GROUP BY project, rooms
        """ .format(days_ago, project['url'])
        res = self.cursor.execute(q)  
        return res

    def count_records(self):
        res = self.cursor.execute("SELECT COUNT(*) FROM flats").fetchall()[0]
        return res[0]

    def get_duplicates(self):  # multiple flat_id records
        q = """
        SELECT
            record_id,
            flat_id,
            date(timestamp, 'unixepoch'),
            timestamp,
            COUNT(*) as "Count"
        FROM flats
        GROUP BY
            flat_id,
            timestamp / (24*60*60)
        HAVING COUNT(*) > 1
        ORDER BY flat_id
        """
        res = self.cursor.execute(q).fetchall()
        return res

    def remove_by_id(self, record_id):
        q = """
        DELETE FROM flats
        WHERE record_id={0}
        """ .format(record_id)
        res = self.cursor.execute(q)  

    def remove_by_date(self, date):  # in format: '2023-05-31'
        q = """
        DELETE FROM flats
        WHERE date(timestamp, 'unixepoch')='{0}'
        """ .format(date)
        res = self.cursor.execute(q) 

    def save_changes(self):
        self.conn.commit()


def load_project_list():
    with open('projects.json', 'r') as f:
        data = json.load(f)
    return data


def download_flats(project, archive_enabled=False):

    def get_ts():
        return datetime.now().strftime('%Y%m%d_%H%M%S')

    result = []
    filenames = []

    if archive_enabled:
        if not os.path.isdir('../archive'):
            os.mkdir('../archive')
    
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
            d = {
                 'project': project['url'],
                 'flat_id': flat['id'],
                 'area': flat['area'],
                 'number': flat['number'],
                 'price': flat['price'],
                 'rooms': flat['rooms'],
                 'floor': flat['floor'],
                 'bulk_id': flat['bulk']['id'],
                 'bulk_title': flat['bulk']['title'],
                 'timestamp': int(datetime.timestamp(datetime.now()))
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
