from cloudant import Cloudant, database
import json
import os

db_name = 'mydb'
client = None
db = None


def Setup() -> database.CouchDatabase:
    """Creates and returns DB"""
    if 'VCAP_SERVICES' in os.environ:
        vcap = json.loads(os.getenv('VCAP_SERVICES'))
        print('Found VCAP_SERVICES')
        if 'cloudantNoSQLDB' in vcap:
            creds = vcap['cloudantNoSQLDB'][0]['credentials']
            user = creds['username']
            # password = creds['password']
            url = 'https://' + creds['host']

            apiKey = creds['apikey']
            # client = cloudant_iam(user, apiKey, url=url, connect=True)
            client = Cloudant.iam(user, apiKey, url=url, connect=True)
            db = client.create_database(db_name, throw_on_exists=False)
    elif "CLOUDANT_URL" in os.environ:
        client = Cloudant.iam(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'],
                              url=os.environ['CLOUDANT_URL'],
                              connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
    elif os.path.isfile('vcap-local.template.json'):
        with open('vcap-local.template.json') as f:
            vcap = json.load(f)
            print('Found local VCAP_SERVICES')
            creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
            user = creds['username']
            # password = creds['password']

            apiKey = creds['apikey']
            url = 'https://' + creds['host']
            # client = Cloudant(user, apiKey, url=url, connect=True)
            client = Cloudant.iam(user, apiKey, url=url, connect=True)
            db = client.create_database(db_name, throw_on_exists=False)

    else:
        print("no db found")

    return db


def Close():
    if client:
        client.disconnect()
